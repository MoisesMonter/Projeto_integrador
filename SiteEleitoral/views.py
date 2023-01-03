from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import FormUser
from Users.models import User as Usuario
# Create your views here.
def Home(request):
    x= int(1)
    return render(request,'home.html',{'x': x})


def Register(request):
    x= int(1)
    if request.method == "GET":
        form = FormUser()
        return render(request,'register.html',{'x': x,'form':form})
    else:
        form = FormUser(request.POST)
        Senha1= request.POST.get('Senha')
        Senha2= request.POST.get('Senha2')
        if Senha1 == Senha2:
            if form.is_valid():
                username = request.POST.get('Id_Academico')
                email = request.POST.get('email') 
                password = request.POST.get('password')   
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                form.save()
                messages.success(request,"Conta Criada com Sucesso")
                return render(request,'login.html',{'x': x,'form':form})
            else:
                label= "senha repetida"
                return render(request,'register.html',{'x':  x,'form':form,'label':label})
        else:
            
            messages.success(request,"Campos repetidos ou atraso no cadastro")
            return render(request,'register.html',{'x':  x,'form':form})

def Login(request):
    if str(request.user) != 'AnonymousUser':
        print(request.user)
        return render(request,"home.html")
    if request.method == "GET":
        return render(request,"login.html")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username =username,password=password)
        print("user = " + str(user)) #always returns None
        if user: # se não for falso
            login_django(request,user)
            return render(request,'home.html')
        else:
            return render(request,'login.html')

def About_us(request):
    x= int(1)
    return render(request,'about_us.html',{'x': x})

def ListaEleicoes(request):
    x= int(1)
    return render(request,'lista_eleicoes.html',{'x': x})



def Suport(request):
    x= int(1)
    return render(request,'suport_site.html',{'x': x})



def plataforma(request):
    log_out = request.POST.get('logout')
    print(log_out)
    if log_out == 'LogOut':
        logout(request)
        return render(request,'login.html')
    if request.user.is_authenticated:
        return render(request,'home.html')