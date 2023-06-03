from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse
from django.contrib import messages
from .forms import *

def loginPage(request):
    return render(request, 'login.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    else: 
        form=createuserform()
        if request.method=='POST':
            form=createuserform(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request, 'registration/register.html', context)
    

# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     else:
#         if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('/')
#             else:
#                 messages.error(request, 'Invalid username or password')
#         return render(request, 'login.html') 
# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')
#     else:
#        if request.method=="POST":
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user=authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             return redirect('/')
#        context={}
#        return render(request,'login.html',context)
   
 
def logoutPage(request):
    logout(request)
    return redirect('/')


def dashboard(request):
    # Add any necessary logic to fetch and process data for the dashboard
    context = {
        # Add any necessary data to pass to the template
    }
    return render(request, 'dashboard.html', context)
 
# def dashboard(request):
   
#     alumnus = Alumni.objects.all()
 
#     context = {
#         'alumnus':alumnus,
#     }
#     return render(request,'alumni/templates/dashboard.html',context)
 
''' def addAlumnus(request):    
    if request.user.is_authenticated:
        form=addAlumnus()
        if(request.method=='POST'):
            form=addAlumnus(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'alumni/addAlumnus.html',context)
    else: 
        return redirect('dashboard')
 '''
 

