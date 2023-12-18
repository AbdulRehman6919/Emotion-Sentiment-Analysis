from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login , logout , authenticate
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
from .fun import getPrediction, getEmotionPrediction
import numpy as np

global percent
percent = -1

global mail
mail = None

def home(request):
    return render(request, 'fyp/home.html')

def tips(request):
    return render(request, 'fyp/tips.html')

def signupuser(request):
    if request.user.is_authenticated:
        return redirect ('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form  = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account is created for ' + user)
                return redirect('loginuser')

        return render(request,'fyp/signupuser.html',{'form':form})
    
def loginuser(request):
    if request.user.is_authenticated:
        return redirect ('home')
    else:
        if request.method == 'POST':
            user = authenticate(username=request.POST['username'],password=request.POST['password'])
            if user is not None:
                login(request , user)
                return redirect ('home')
            else:
                messages.info(request,'Username or password is incorrect')
        return render(request,'fyp/loginuser.html')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def fileupload(request):

    return render(request, 'fyp/fileupload.html')


def result(request):

    # file upload
     if request.method == "POST":
        try:
            if not request.FILES['input2'].name.endswith('.txt'):

                return render(request,'fyp/fileupload.html',{'error':'Only .txt format file is allowed'})
            else:
                my_uploaded_file = request.FILES['input2'] # get the uploaded file
                string = re.findall(r"\S+", my_uploaded_file.read().decode("utf-8"))
                string = ' '.join(string)

                print(string)
                print(request.POST.dict().keys())

                if "hateful" in request.POST.dict().keys():
                    result = getPrediction(string)
                    return render(request,'fyp/hateful_result.html', {'txt':result})
                elif "emotion" in request.POST.dict().keys():
                    result = getEmotionPrediction(string)
                    return render(request,'fyp/emotions_result.html', {'txt':result})

        except Exception as e:
                print('Error:'+ str(e))
     
     # Written Text.
     else:
         txt = request.GET.get('input1')

         if txt == '':
            return render(request, 'fyp/home.html',{'error': 'Please enter a message'})
         else:

            if "hateful" in request.GET.dict().keys():
                result = getPrediction(txt)
                return render(request,'fyp/hateful_result.html', {'txt':result})
            elif "emotion" in request.GET.dict().keys():
                result = getEmotionPrediction(txt)
                return render(request,'fyp/emotions_result.html', {'txt':result})
            else:
                return render(request, 'fyp/home.html', {'error': 'Coming Soon....'})

def contact(request):
    return render(request,'fyp/contact.html')
