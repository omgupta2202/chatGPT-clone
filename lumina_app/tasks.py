from celery import shared_task
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import ChatLog, DocumentExport
import logging

logger = logging.getLogger(__name__)

@shared_task
def generate_chat_export_pdf(chatlog_id, export_id):
    """
    Asynchronous task pipeline to generate a PDF export of a chat transcript.
    This offloads compute-heavy exports to maintain sub-second UI responsiveness.
    """
    try:
        chatlog = ChatLog.objects.get(id=chatlog_id)
        export = DocumentExport.objects.get(id=export_id)
        
        # In-memory file for PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        
        # Simple PDF generation
        y_position = 800
        p.drawString(100, y_position, f"Chat Export: {chatlog.title}")
        y_position -= 30
        
        for msg in chatlog.messages.all():
            text = f"{msg.user if msg.user else 'User'}: {msg.content[:100]}..." # Truncating for simplicity
            p.drawString(100, y_position, text)
            y_position -= 20
            
            if y_position < 50:
                p.showPage()
                y_position = 800
                
        p.showPage()
        p.save()
        
        pdf_name = f"chat_{chatlog_id}_export.pdf"
        export.file.save(pdf_name, ContentFile(buffer.getvalue()))
        export.status = 'COMPLETED'
        export.save()
        
        return f"Successfully exported ChatLog {chatlog_id}"
    
    except Exception as e:
        logger.error(f"Error in async document export: {e}")
        export = DocumentExport.objects.get(id=export_id)
        export.status = 'FAILED'
        export.save()
        return str(e)
