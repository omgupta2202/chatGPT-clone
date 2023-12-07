from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .gpt_util import get_response
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from .models import ChatLog, ChatMessage

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
            return render(request, 'newAI_app/sign-up.html')

    return render(request, "newAI_app/sign-up.html")

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
            return render(request, "newAI_app/sign-in.html")
    return render(request, "newAI_app/sign-in.html")


def logout_view(request):
    logout(request)
    return redirect('/login')

def index(request):
    if request.method == 'POST':
        prompt = request.POST.get('user-prompt')
        response = get_response(prompt)
        if response:
            ChatHistory.objects.create(user=request.user, usermsg=prompt, display_msg=response)
            data = {"usermsg": prompt, "display_msg": response, "user": request.user.username}
            return JsonResponse({'data': data})
        else:
            return JsonResponse({'error': 'something went wrong'}, status=400)

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    previous_chats_today = ChatLog.objects.filter(start_time__date=today, user=request.user)
    previous_chats_yesterday = ChatLog.objects.filter(start_time__date=yesterday, user=request.user)
    previous_chats = ChatLog.objects.filter(start_time__date__lt=yesterday, user=request.user)

    return render(request, 'newAI_app/dashboard.html', {
        'previous_chats_today': previous_chats_today,
        'previous_chats_yesterday': previous_chats_yesterday,
        'previous_chats': previous_chats,
    })

def chat_view(request, chatlog_id=None):
    if chatlog_id:
        chatlog = get_object_or_404(ChatLog, pk=chatlog_id, user=request.user)
        messages = chatlog.messages.all()
        previous_chats_today = ChatLog.objects.filter(start_time__date=datetime.now().date(), user=request.user)
        previous_chats_yesterday = ChatLog.objects.filter(start_time__date=(datetime.now().date() - timedelta(days=1)), user=request.user)
        previous_chats = ChatLog.objects.filter(start_time__date__lt=(datetime.now().date() - timedelta(days=1)), user=request.user)
        
        return render(request, 'your_template.html', {
            'chatlog': chatlog,
            'messages': messages,
            'previous_chats_today': previous_chats_today,
            'previous_chats_yesterday': previous_chats_yesterday,
            'previous_chats': previous_chats,
        })
    else:
        return render(request, "newAI_app/dashboard.html")