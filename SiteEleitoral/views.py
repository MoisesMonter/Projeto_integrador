from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import FormUser,Senha_padrao
from Users.models import User as Usuario
# Create your views here.
def Home(request):
    x= int(1)
    return render(request,'home.html',{'x': x})


def Register(request):
    x= int(1)
    if request.method == "GET":
        form = FormUser()
        Senha= Senha_padrao
        return render(request,'register.html',{'x': x,'form':form,'senha':Senha})
    else:
        form = FormUser(request.POST)
        if form.is_valid():
            '''usuario = form.save()
            user = User.objects.create_user(form.object(Id), email=email, password=senha)
            user.save()'''
            senha = request.POST['Senha']
            return HttpResponse(f"{senha}")
            '''return render(request,'login.html',{'x': x,'form':form})'''
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
