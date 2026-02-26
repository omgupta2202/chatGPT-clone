from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .gpt_util import get_response
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from .models import ChatLog, ChatMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.


def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password_repeat = request.POST.get("password2")
        user = CustomUser.objects.filter(email=email)
        if user.exists():
            messages.info(request, "User already Exists, Please login!")
            return redirect('/')

        if password == password_repeat and len(password) >= 8:
            user = CustomUser.objects.create_user(
                first_name=name,
                email=email,
                password=password,
            )
            return redirect('/')
        else:
            messages.error(request, "your password is too short")
            return render(request, 'lumina_app/sign-up.html')

    return render(request, "lumina_app/sign-up.html")

def signin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_user = authenticate(request, email=email, password=password)
        user = CustomUser.objects.filter(email=email)

        if is_user is not None:
            login(request, is_user)
            return redirect('/home')

        if not user.exists():
            messages.info(request, "User does not exist, Please Signup First!")
            return redirect('/sign-up')

        elif is_user is None:
            messages.info(request, 'Email or Password is incorrect!')
            return render(request, "lumina_app/sign-in.html")
    return render(request, "lumina_app/sign-in.html")


def logout_view(request):
    logout(request)
    return redirect('/')

def get_previous_chats(user):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    previous_chats_today = ChatHistory.objects.filter(date_created__date=today, user=user)
    previous_chats_yesterday = ChatHistory.objects.filter(date_created__date=yesterday, user=user)
    previous_chats = ChatHistory.objects.filter(date_created__date__lt=yesterday, user=user)
    
    # Update titles based on the first message text of the user
    for chat in previous_chats_today:
        chat.title = chat.usermsg.split('\n')[0]  # Assuming title is the first line of the user message
        chat.save()

    for chat in previous_chats_yesterday:
        chat.title = chat.usermsg.split('\n')[0]
        chat.save()

    for chat in previous_chats:
        chat.title = chat.usermsg.split('\n')[0]
        chat.save()
    
    return {
        'previous_chats_today': previous_chats_today,
        'previous_chats_yesterday': previous_chats_yesterday,
        'previous_chats': previous_chats,
    }

@login_required
def index(request):
    chats_data = get_previous_chats(request.user)
    if request.method == 'POST':
        prompt= request.POST.get('user-prompt')
        title = request.POST.get('user-prompt')
        response = get_response(prompt)
        if response:
            chat_history = ChatHistory.objects.create(user=request.user, usermsg=prompt, display_msg=response)
            data = {
                "id": chat_history.id,
                "usermsg": prompt,
                "display_msg": response,
                "user": request.user.username,
                "title": title.split('\n')[0]
            }
            return JsonResponse({'data': data})
        else:
            return JsonResponse({'error': 'something went wrong'}, status=400)
    return render(request, 'lumina_app/dashboard.html', chats_data)

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        UserModel = get_user_model()
        user_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
        }
        print(request.POST.get('username'))  # Debugging: Check the username received from the form

        user = UserModel.objects.get(pk=user.pk)
        for field, value in user_data.items():
            setattr(user, field, value)
        
        user.save()
        print(user.username)  # Debugging: Check the updated username after saving
        return redirect('home')
    
    return redirect('home')


def chat_view(request, chatlog_id=None):
    user = request.user
    if chatlog_id:
        chatlog = get_object_or_404(ChatLog, pk=chatlog_id, user=request.user)
        messages = chatlog.messages.all()
        previous_chats_today = ChatLog.objects.filter(start_time__date=datetime.now().date(), user=request.user)
        previous_chats_yesterday = ChatLog.objects.filter(start_time__date=(datetime.now().date() - timedelta(days=1)), user=request.user)
        previous_chats = ChatLog.objects.filter(start_time__date__lt=(datetime.now().date() - timedelta(days=1)), user=request.user)
        
        return render(request, 'lumina_app/dashboard.html', {
            'user': user,
            'chatlog': chatlog,
            'messages': messages,
            'previous_chats_today': previous_chats_today,
            'previous_chats_yesterday': previous_chats_yesterday,
            'previous_chats': previous_chats,
        })
    else:
        return render(request, "lumina_app/dashboard.html")
    
def delete_chat(request, chat_id):
    try:
        chat = ChatHistory.objects.get(id=chat_id)
        chat.delete()
        return JsonResponse({'message': 'Chat deleted successfully'})
    except ChatHistory.DoesNotExist:
        return JsonResponse({'error': 'Chat does not exist'}, status=404)
    
def get_conversation(request):
    chat_id = request.GET.get('chatId')
    try:
        conversation = ChatHistory.objects.get(id=chat_id)
        conversation_data = {
            'id': conversation.id,
            'user': conversation.user.username,
            'usermsg': conversation.usermsg,
            'display_msg': conversation.display_msg,
            # Add other fields from ChatHistory model as needed
        }
        print (conversation_data)

        return JsonResponse({'data': conversation_data})  # Return the conversation data as JSON
    except ChatHistory.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found'}, status=404)