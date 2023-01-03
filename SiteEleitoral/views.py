from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import FormUser
# Create your views here.
def Home(request):
    x= int(1)
    return render(request,'home.html',{'x': x})

@csrf_exempt
def Register(request):
    x= int(1)
    if request.method == "GET":
        form = FormUser()
        return render(request,'register.html',{'x': x,'form':form})
    else:
        form = FormUser(request.POST)
        if form.is_valid():
            usuario = form.save()
            form = FormUser()
        else:
            return render(request,'register.html',{'x': x,'form':form})
def About_us(request):
    x= int(1)
    return render(request,'about_us.html',{'x': x})

def ListaEleicoes(request):
    x= int(1)
    return render(request,'lista_eleicoes.html',{'x': x})

def Login(request):
    x= int(1)
    return render(request,'login.html',{'x': x})

def Suport(request):
    x= int(1)
    return render(request,'suport_site.html',{'x': x})


def _get_failure_view():
    """
    Returns the view to be used for CSRF rejections
    """
    return get_callable(settings.CSRF_FAILURE_VIEW)