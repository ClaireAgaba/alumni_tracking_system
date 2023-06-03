from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from alumni.EmailBackend import EmailBackEnd
from .forms import *


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            
        else:
                messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
        return redirect('login')


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard') 
#     else: 
#         form=createuserform()
#         if request.method=='POST':
#             form=createuserform(request.POST)
#             if form.is_valid() :
#                 user=form.save()
#                 return redirect('login')
#         context={
#             'form':form,
#         }
#         return render(request, 'registration/register.html', context)
    

# # def loginPage(request):
# #     if request.user.is_authenticated:
# #         return redirect('/')
# #     else:
# #         if request.method == "POST":
# #             username = request.POST.get('username')
# #             password = request.POST.get('password')
# #             user = authenticate(request, username=username, password=password)
# #             if user is not None:
# #                 login(request, user)
# #                 return redirect('/')
# #             else:
# #                 messages.error(request, 'Invalid username or password')
# #         return render(request, 'login.html') 
# # def loginPage(request):
# #     if request.user.is_authenticated:
# #         return redirect('dashboard')
# #     else:
# #        if request.method=="POST":
# #         username=request.POST.get('username')
# #         password=request.POST.get('password')
# #         user=authenticate(request,username=username,password=password)
# #         if user is not None:
# #             login(request,user)
# #             return redirect('/')
# #        context={}
# #        return render(request,'login.html',context)
   
 
# def logoutPage(request):
#     logout(request)
#     return redirect('/')


# def dashboard(request):
#     # Add any necessary logic to fetch and process data for the dashboard
#     context = {
#         # Add any necessary data to pass to the template
#     }
#     return render(request, 'dashboard.html', context)
 
# # def dashboard(request):
   
# #     alumnus = Alumni.objects.all()
 
# #     context = {
# #         'alumnus':alumnus,
# #     }
# #     return render(request,'alumni/templates/dashboard.html',context)
 
# ''' def addAlumnus(request):    
#     if request.user.is_authenticated:
#         form=addAlumnus()
#         if(request.method=='POST'):
#             form=addAlumnus(request.POST)
#             if(form.is_valid()):
#                 form.save()
#                 return redirect('/')
#         context={'form':form}
#         return render(request,'alumni/addAlumnus.html',context)
#     else: 
#         return redirect('dashboard')
