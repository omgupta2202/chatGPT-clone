from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_recaptcha.fields import ReCaptchaField
from django.forms import Form
from .models import ChatLog, ChatMessage, DocumentExport
from .serializers import ChatLogSerializer, DocumentExportSerializer
from .tasks import generate_chat_export_pdf
from .services.llm_router import LLMRouter

class ReCaptchaForm(Form):
    captcha = ReCaptchaField()

class ChatAPIView(APIView):
    """
    Handles prompt submissions.
    Expects JWT authentication and an optional recapcha token.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt')
        chatlog_id = request.data.get('chatlog_id')
        recaptcha_token = request.data.get('g-recaptcha-response')
        
        # Simple ReCaptcha validation (mock using a form)
        form = ReCaptchaForm(data={'captcha': recaptcha_token})
        # For local dev we silenced the errors, but this is how we would mitigate bot abuse
        if recaptcha_token and not form.is_valid():
             return Response({"error": "Invalid reCAPTCHA"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create chatlog
        if chatlog_id:
            try:
                chatlog = ChatLog.objects.get(id=chatlog_id, user=request.user)
            except ChatLog.DoesNotExist:
                return Response({"error": "ChatLog not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            chatlog = ChatLog.objects.create(user=request.user, title=prompt[:50])
            
        # Store user message
        ChatMessage.objects.create(chat_log=chatlog, content=prompt, user=request.user)
        
        # Build memory (last 5 messages for context)
        history = list(chatlog.messages.all().order_by('time'))[-6:-1]
        chat_history = [{"role": "user" if msg.user else "assistant", "content": msg.content} for msg in history]
        
        # Generate LLM response
        router = LLMRouter()
        response_text = router.generate_response(prompt=prompt, chat_history=chat_history)
        
        # Store AI response
        ai_message = ChatMessage.objects.create(chat_log=chatlog, content=response_text)
        
        # Return serialized data
        return Response({
            "chatlog_id": chatlog.id,
            "response": response_text
        }, status=status.HTTP_200_OK)

class ExportChatAPIView(APIView):
    """
    Triggers an asynchronous export of a ChatLog to PDF.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, chatlog_id):
        try:
            chatlog = ChatLog.objects.get(id=chatlog_id, user=request.user)
        except ChatLog.DoesNotExist:
            return Response({"error": "ChatLog not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Create a pending document export record
        export = DocumentExport.objects.create(
            chat_log=chatlog,
            user=request.user,
            status='PENDING'
        )
        
        # Trigger Celery Task Pipeline
        generate_chat_export_pdf.delay(chatlog.id, export.id)
        
        # Return export ID to client for polling
        return Response({
            "message": "Export started",
            "export_id": export.id
        }, status=status.HTTP_202_ACCEPTED)

class ExportStatusAPIView(generics.RetrieveAPIView):
    """
    Retrieves the status of an asynchronous document export.
    """
    queryset = DocumentExport.objects.all()
    serializer_class = DocumentExportSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
         return self.queryset.filter(user=self.request.user)
