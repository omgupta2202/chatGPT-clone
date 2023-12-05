from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .gpt_util import get_response

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

# def index(request):
#     if request.method == 'POST':
#         prompt = request.POST.get('user-prompt')
#         response = get_response(prompt)
#         if response:
#             chat = ChatHistory.objects.create(user=request.user, usermsg=prompt, display_msg=response)
#             for i in ChatHistory.objects.filter(user=request.user)
#                 data = {"usermsg":usermsg,"display_msg":display_msg,"user":user}
#             return JsonResponse({'data': data})
#         else:
#             return JsonResponse({'error': 'Incident ID not provided'}, status=400)
#     return render(request, "newAI_app/dashboard.html")


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

    return render(request, "newAI_app/dashboard.html")


# from django.shortcuts import render, HttpResponse

# from django.views.decorators.csrf import csrf_exempt

# from .models import ChatHistory, PromptHistory

# import json


# @csrf_exempt
# def chat(request):
#     if request.method == 'POST':
#
#         # Handle incoming message
#
#         data = json.loads(request.body.decode('utf-8'))
#
#         # message = request.POST.get('message', '')
#         message = "HELLO"
#         if message:
#             response = get_response(message)
#             chat = ChatHistory.objects.create(user=request.user, display_msg="this is the demo title")
#             PromptHistory.objects.create(chat=chat, user_prompt=message, gpt_response=response)
#
#             return HttpResponse(status=201)
#
#         else:
#
#             return HttpResponse(status=400)
#
#     elif request.method == 'GET':
#
#         # Return all chat messages
#
#         messages = PromptHistory.objects.all()
#
#         message_list = [{'sender': request.user.email, 'message': msg.user_prompt} for msg in messages]
#
#         return HttpResponse(json.dumps(message_list), content_type='application/json')
#
#     return HttpResponse(status=400)
