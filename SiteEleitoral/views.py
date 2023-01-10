from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import FormUser,FormLogin,FormImagem,Formulario_part1,Formulario_part2,Formularios_Para_Votar,Select_day,Botoes_Urna
from Users.models import User as Usuario
from Users.models import Election,Data_Election,Interaction_User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm  
# Create your views here.
import datetime,re

def Logout(request):
    logout(request)
    return Login(request)


def Home(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"home.html",{'x':False})
    else:
        try:
            
            usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
            #user_all_info=[str(x) for x in User.objects.filter(username__contains="0")] quando letra tá maiuscula
            #usuario_logado = usuario_logado.bojects.filter(Id_Academico = str(request.user))
            #return HttpResponse(f"{usuario_logado[0:2]}")
            return render(request,"home.html",{'x':True,'usuario_logado':usuario_logado})
        except:
            
            return render(request,"home.html",{'x':True})



def Register(request):
    x =str(request.user) == 'AnonymousUser'
    if str(request.user) != 'AnonymousUser':
        try:
            
            usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
            #user_all_info=[str(x) for x in User.objects.filter(username__contains="0")] quando letra tá maiuscula
            #usuario_logado = usuario_logado.bojects.filter(Id_Academico = str(request.user))
            #return HttpResponse(f"{usuario_logado[0:2]}")
            return render(request,"home.html",{'x':True,'usuario_logado':usuario_logado})
        except:
            
            return render(request,"home.html",{'x':True})
    if request.method == "GET":
        form = FormUser()
        x= str(request.user) != 'AnonymousUser'
        return render(request,'register.html',{'x': False,'form':form})
    else:

        form = FormUser(request.POST)
        username = request.POST.get('Id_Academico')
        email = request.POST.get('email') 
        password = request.POST.get('Senha')  
        if request.POST.get('Senha') == request.POST.get('Senha2'):
            if form.is_valid():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                form.save()       
                messages.success(request,"Conta Criada com Sucesso")
                return render(request,'login.html',{'x': False,'form':form})
            else: 
                messages.success(request,"Erro de Autenticação no Formulário")
                return render(request,'register.html',{'x': False,'form':form})
        else:
            messages.success(request,"Senhas não combinam")
            return render(request,'register.html',{'x': False,'form':form})


def Login(request):
    form = FormLogin(request.POST)
    if str(request.user) != 'AnonymousUser':
        return render(request,"home.html",{'x':True,"form":form})
    else:
        
        if request.method == "GET":
            return render(request,"login.html",{"form":form})
        

        if request.method == 'POST':
            username = request.POST.get('Id_Academico')
            password = request.POST.get('Senha')  
            user = authenticate(request, username = username,password = password)
            if user is not None:
                login_django(request,user)
                usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
                return render(request,"home.html",{'x':True,'usuario_logado':usuario_logado})
            return render(request,"login.html",{"form":form})


def About_us(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,'about_us.html',{'x': False})
    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        return render(request,"about_us.html",{'x':True,'usuario_logado':usuario_logado})




def ListaEleicoes(request):

    
    x =str(request.user) == 'AnonymousUser'
    if x:

        info = ações_Usuarios(str(request.user),'sim').global_list(request)
        enviar_para_Urna = Formularios_Para_Votar(request.POST)
        aux = request.POST.get('Form1')
        aux2 = str(request.POST.get('local_urna'))
        if aux != None and aux2 !=None:
            #print(aux,aux2)
            aux = ações_Usuarios(str(request.user),'sim').global_list_urna(request,aux2,'Lista_Eleicoes',True)

        #print(aux2)        
        if request.method == 'GET':

            return render(request,"lista_eleicoes.html",{'x':False,'TheList':info,'Urna':enviar_para_Urna})

        if request.method =='POST':
            aux = request.POST.get('Form2')
            aux2 = request.POST.get('local_urna')
            if aux2 !=None:
                #print(aux,aux2)
                ações_Usuarios(str(request.user),'sim').global_list_urna(request,aux2,'lista_eleicoes',True)
                return Urna(request)
        return render(request,"lista_eleicoes.html",{'x':False,'TheList':info,'Urna':enviar_para_Urna})
    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        info = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_list(request)
        enviar_para_Urna = Formularios_Para_Votar(request.POST)


        if request.method == 'GET':

            return render(request,"lista_eleicoes.html",{'x':True,'usuario_logado':usuario_logado,'TheList':info,'Urna':enviar_para_Urna})
        
            
        if request.method =='POST':
            aux = request.POST.get('Form2')
            aux2 = request.POST.get('local_urna')
            if aux2 !=None:
                #print(aux,aux2)
                ações_Usuarios(str(request.user),'sim').global_list_urna(request,aux2,'lista_eleicoes',True)
                return Urna(request)
            #print(aux)
            usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
            
            return render(request,"lista_eleicoes.html",{'x':True,'usuario_logado':usuario_logado,'TheList':info,'Urna':enviar_para_Urna})
            
        ''' for Number in range(0,int(todas_eleicoes),1):
        print(Number)'''
        return render(request,"lista_eleicoes.html",{'x':True,'usuario_logado':usuario_logado,'TheList':info,'Urna':enviar_para_Urna})
 



def Urna(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"Urna.html",{'x':False})
    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        formularios = Formularios_Para_Votar(request.POST)
        info_Rapida = ações_Usuarios(str(request.user),'sim').global_list_urna(request,'','',False)
        info_eleicao = Election.objects.get(N_Eleicao = info_Rapida[0])
        botoes_urna = Botoes_Urna(request.POST)
        info_candidatos,info_candidatos_apurados = ações_Usuarios(str(request.user),info_Rapida[1]).lista_candidatos(request,info_Rapida[0])
        #print(info_candidatos)
        form = 0
        interacao_usuario=[]
        local = []
        try:

            if request.POST.get('Form1') != None:
                form = 1
                interacao_usuario = Interaction_User.objects.all().filter(Usuario = usuario_logado,N_Eleicao =info_eleicao).values_list()        
            else:
                form = 0
            print('aqui...',info_candidatos)
            print("eleicao..",info_eleicao)
            if len(interacao_usuario) != 0:
                print('achado!!!!!')
                form = 0
                messages.success(request,f"Você Não pode Participar duas vezes")
            if request.method =='GET':
                if request.method =='GET':
                    print("opa")
                return render(request,"Urna.html",{'x':True,'local':info_Rapida[1],'candidatos':info_candidatos,'Eleitoral':info_eleicao,'form_1':1 ,'formularios':formularios,'usuario_logado':usuario_logado,'botoes_urna':botoes_urna})
            if botoes_urna != None:
                if request.POST['Null'] != None:
                    print(request.POST['Null'])
                if request.POST['b0'] != None:
                    print(request.POST['b0'])
                if request.POST['b1'] != None:
                    print(request.POST['b1'])
                if request.POST['b2'] != None:
                    print(request.POST['b2'])
                if request.POST['b3'] != None:
                    print(request.POST['b3'])
                if request.POST['b4'] != None:
                    print(request.POST['b4'])
                if request.POST['b5'] != None:
                    print(request.POST['b5'])
                if request.POST['b6'] != None:
                    print(request.POST['b6'])
                if request.POST['b7'] != None:
                    print(request.POST['b7'])
                if request.POST['b8'] != None:
                    print(request.POST['b8'])
                if request.POST['b9'] != None:
                    print(request.POST['b9'])

            return render(request,"Urna.html",{'x':True,'local':info_Rapida[1],'candidatos':info_candidatos,'Eleitoral':info_eleicao,'form_1':1,'formularios':formularios,'usuario_logado':usuario_logado,'botoes_urna':botoes_urna})
                
        except:
            #print(formularios.Form1)
            return render(request,"Urna.html",{'x':True,'local':info_Rapida[1],'candidatos':info_candidatos,'Eleitoral':info_eleicao,'form_1':form,'formularios':formularios,'usuario_logado':usuario_logado,'botoes_urna':botoes_urna})


def gerarumaeleicao(request):
    x =str(request.user) == 'AnonymousUser'
    if x == True:
        return render(request,"gerarumaeleicao.html",{'x':False})  

    else:

        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        select_day = Select_day(request.POST)
        titulo = request.POST.get('Formulario1')
        descricao = request.POST.get('Formulario2')
        lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,'',[],False,False)
        lista_informacoes = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info2(request,'','',False)
        print(lista_informacoes)
        titulo = request.POST.get('Formulario1')
        descricao = request.POST.get('Formulario2')
        if request.method =='GET':
            try:
                
                
                return render(request,"gerarumaeleicao.html",{'x':True,'select_day':select_day,'form1':Formulario_part1,'form1_2':lista_informacoes,'form2':Formulario_part2,'form3':   Formularios_Para_Votar,'usuario_logado':usuario_logado,'lista_candidatos':lista_candidatos,'len':len(lista_candidatos)})
            except:
                lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,request.POST.get('__Candidato__'),[],False,False)
            
            
            return render(request,"gerarumaeleicao.html",{'x':True,'select_day':select_day,'form1':Formulario_part1,'form1_2':lista_informacoes,'form2':Formulario_part2,'form2':Formulario_part2,'usuario_logado':usuario_logado,'lista_candidatos':lista_candidatos,'len':0})      
        if request.method == 'POST':
            if Formulario_part2(request.POST).is_valid():
                candidato = request.POST.get('Gerando_Candidato')
                
                lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,candidato,[],False,False)

                #form1 =  Formulario_part1(request.POST)
            if Select_day(request.POST).is_valid(): 

                
                lista_informacoes = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info2(request,titulo,descricao,False)
                lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,'',[],True,False)
                titulo = lista_informacoes[0]
                descricao=lista_informacoes[1]
                dias = datetime.timedelta(int(request.POST.get('select_day')))
                data = datetime.datetime.now()


                
                if len(titulo) >0:

                    if len(lista_candidatos) >1:
                        import random
                        lista_numero=[]
                        while len(lista_numero)< len(lista_candidatos):
                            sorteio = random.randint(1,100)
                            if sorteio not in lista_numero:
                                lista_numero.append(sorteio)
    

                
                        try:
                            for info in Election.objects.all():##Informando o Ultimo ID de todos elementos da Eleição
                                id_end = info
                            id_end =  int(re.sub('[^0-9]',' ', str(id_end)))+1

                            formulario_eleicao =Election(N_Eleicao= id_end,Usuario =  usuario_logado,Titulo = titulo,Data = data,End_Data = data+dias, Descricao=descricao, Ativo=True,Disponibilizar=False)
                            formulario_eleicao.save()

                            lista_numero.append(0)
                            lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,'Null',[],True,False)
                            print(lista_numero)
                            print(lista_candidatos)
                            for x in range (0,len(lista_numero),1):
                                formulario_deep = Data_Election(N_Eleicao = formulario_eleicao,Candidatos=lista_candidatos[x],N_Candidato=lista_numero[x],Votos=0)
                                formulario_deep.save()
                            '''for eleitor,n_eleitoral in zip(lista_candidatos,lista_numero):
                                formulario_aprofundado_eleicao= Data_Election(N_Eleicao = formulario_eleicao,Candidatos=eleitor,N_Candidato = n_eleitoral,Votos=0)    
                                formulario_aprofundado_eleicao.save()'''
                            messages.success(request,f"{titulo} Criada com sucesso!")
                        except:
                            for eleitor,n_eleitoral in zip(lista_candidatos,lista_numero):
                                formulario_aprofundado_eleicao= Data_Election(N_Eleicao = formulario_eleicao,Candidatos=eleitor,N_Candidato = n_eleitoral,Votos=0)    
                                formulario_aprofundado_eleicao.save()
                            messages.success(request,f"{titulo} Criada com sucesso!")    
                        ações_Usuarios(str(usuario_logado.Id_Academico),'sim').limpar_memoria(request,"apagar_lista_texto")
                        lista_informacoes = []
                        ações_Usuarios(str(usuario_logado.Id_Academico),'sim').limpar_memoria(request,"apagar_lista_candiatos")
                        lista_candidatos = []
                        id_end = 0
                    else:
                        messages.success(request,"Candidatos insuficientes! tenha ao menos 2!")
                else:
                    messages.success(request,"Campos vazios")
                
                #formulario_eleicao =Election(N_Eleicao= id_end,Usuario =  usuario_logado,Titulo = titulo,Data = data,End_Data = data+dias, Descricao=descricao, Ativo=True,Disponibilizar=False)
                #formulario_eleicao.save()
                '''formulario_eleicao.Usuario = request.user
                formulario_eleicao.Titulo = request.POST.get('Titulo')
                formulario_eleicao.Descricao= request.POST.get('Texto')
                formulario_eleicao.Data = datetime.datetime.now()
                formulario_eleicao = GerarUmaEleicao(Usuario=  request.user,)
                print('\n\n\n',formulario_eleicao.Usuario,'\n',
                                formulario_eleicao.Titulo,'\n',
                                formulario_eleicao.Descricao,'\n',
                                formulario_eleicao.Data)
                eleicao_criada = formulario_eleicao.save()'''
            #   if request.method == 'POST':
            titulo = request.POST.get('Formulario1')
            #print(titulo)
            descricao = request.POST.get('Formulario2')
            #print(descricao)
            lista_informacoes = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info2(request,titulo,descricao,True)

            lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,'',[],False,False)
            #print(lista_informacoes,'\n\n\n\n\n')
            '''try:
                lista =lista_candidatos[usuario_logado.Id_Academico]
            except:
                lista=[]'''
            #print(lista)
            try:
                if request.POST.get('Form1') != None:
                    lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').limpar_memoria(request,'apagar_lista_candiatos')
                    lista_candidatos=[]
                    return render(request,"gerarumaeleicao.html",{'x':True,'select_day':select_day,'form1':Formulario_part1,'form1_2':lista_informacoes,'form2':Formulario_part2,'form3':   Formularios_Para_Votar,'usuario_logado':usuario_logado,'lista_candidatos':lista_candidatos,'len':len(lista_candidatos)})
                else:
                    for x in lista_candidatos:
    
                        if str(request.POST.get(str(x))) == "on":
                            lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,x,[],True,False)
                        
                        

            except:
                for x in lista_candidatos:
                    
                    if str(request.POST.get(str(x))) == "on":
                        lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,x,[],True,False)
        return render(request,"gerarumaeleicao.html",{'x':True,'select_day':select_day,'form1':Formulario_part1,'form1_2':lista_informacoes,'form2':Formulario_part2,'form3':   Formularios_Para_Votar,'usuario_logado':usuario_logado,'lista_candidatos':lista_candidatos,'len':len(lista_candidatos)})   







        
def Suport(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,'suport_site.html',{'x': False})
    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        return render(request,"suport_site.html",{'x':True,'usuario_logado':usuario_logado})



def Config(request):
    if str(request.user) == 'AnonymousUser':
        return render(request,"config.html",{'x':False})
    if str(request.user) != 'AnonymousUser':
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        atual_cpf = str(usuario_logado.CPF)
        cpf_usuario=''
        for x in range (0,11,1):
            cpf_usuario += atual_cpf[x]
            if x ==2 or x == 5:
                cpf_usuario +='.'
            elif x == 8:
                cpf_usuario+='-'
        senha_usuario = ''.join(['*' for x  in range(0,len(str(usuario_logado.Senha)),1)])
        form = FormImagem(request.POST,request.FILES)
        if form.is_valid():
            '''usuario_logado.Foto.delete()'''
            usuario_logado.Foto.delete()
            usuario_logado.Foto = request.FILES['Foto']
            usuario_logado.save()
            form = FormImagem()
            print('\n\n\n',form)
        return render(request,"config.html",{'x':True,'form':form,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario),'cpf_usuario':cpf_usuario}) 
    else:
        
        print('\n\nfora')
        print('\n\nfora')
        if form.is_valid():
            form = FormImagem() 

    return render(request,"config.html",{'x':True,'form':form,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario),'cpf_usuario':cpf_usuario}) 


def configkey(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"configkey.html",{'x':False})
    else:
        try:
            usuario_logado= Usuario.objects.get(Id_Academico = request.user)
            senha_usuario = ''.join(['*' for x  in range(0,len(str(usuario_logado.Senha)),1)])
            
            if request.method == 'POST':
                password_local=request.POST.get('password')
                password_new=request.POST.get('n_password')
                password_rep=request.POST.get('r_password')
                import os
                os.system('cls')

                if password_local == usuario_logado.Senha:
                    if str(password_new) ==str(password_rep):
                        Super_User = User.objects.get(username= str(request.user))
                        Super_User.set_password(str(request.POST['n_password']))
                        usuario_logado.Senha = request.POST['n_password']
                        Super_User.save()
                        usuario_logado.save()
                        messages.success(request,"Senha atualizada com Sucesso")
                        return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})
                    else:
                        messages.success(request,"Novas Senhas não combinam")
                        messages.success(request,"Tente novamente.")   
                        return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})
                else:
                    messages.success(request,"Essa não é sua senha Atual")

                    return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})
            
            else:
                return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})   
        except:
            return render(request,"configkey.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})    
    


def configdel(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"config_del.html",{'x':False})
    else:
        try:
            usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
            senha_usuario = ''.join(['*' for x  in range(0,len(str(usuario_logado.Senha)),1)])
            
            if request.method == 'POST':
                password_local=request.POST.get('password')
                confirm = request.POST.get('checkbox')
                print('\n\n\n\n',confirm)
                if password_local == usuario_logado.Senha:
                    if str(confirm) == 'on':
                        messages.success(request,"Conta apagada")
                        Super_User = User.objects.get(username= str(request.user))
                        #usuario_logado.delete()
                        #Super_User.delete()
                        return render(request,'login.html')
                        
                    else:
                        messages.success(request,"Checkbox não autenticado")
                        messages.success(request,"Tente novamente.")
                else:
                    messages.success(request,"Essa não é sua senha")
                    messages.success(request,"Tente novamente.")

            return render(request,"config_del.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})    
            
        except:

            return render(request,"config_del.html",{'x':True,'usuario_logado':usuario_logado,'senha_usuario':str(senha_usuario)})    


def plataforma(request):
    log_out = request.POST.get('logout')
    print(log_out)
    if log_out == 'LogOut':
        logout(request)
        return render(request,'login.html')
    if request.user.is_authenticated:
        return render(request,'home.html')


class ações_Usuarios():
    gerando_lista_candidatos = {}
    gerando_informacoes_candidatura = {}
    local_atual_eleicao = {}
    requisições={}
    def __init__(self,login,pagina_atual):
        global gerando_lista_candidatos
        global gerando_informacoes_candidatura
        global local_atual_eleicao
        self.login = login
        self.pagina_atual = pagina_atual

    def limpar_memoria(self,request,select):
        if select == "apagar_lista_candiatos":
            self.gerando_lista_candidatos.pop(self.login)
        if select == "apagar_lista_texto":
            self.gerando_informacoes_candidatura.pop(self.login)

    def global_info(self,request,info,info_local,manipulacao,login_end):
        if self.login not in self.gerando_lista_candidatos:
            self.gerando_lista_candidatos[self.login]=[]
        if info != None and info != '' and len(info) >0:
            try:
                info_local = self.gerando_lista_candidatos[self.login]
                if manipulacao == True: #caso seja necessario apagar
                    info_local.remove(info)
                else:#caso contrario apenas incremente
                    if info not in info_local:
                        info_local.append(info)
                        self.gerando_lista_candidatos[self.login]=info_local
                    else:
                        messages.success(request,"Usuário Repetido")
            except:
                info_local.append(info)
                self.gerando_lista_candidatos[self.login]=info_local

        return self.gerando_lista_candidatos[self.login]

    def global_info2(self,request,titulo,Texto,modificar):
        if self.login not in self.gerando_informacoes_candidatura:
            self.gerando_informacoes_candidatura[self.login]=['','']


        if modificar == True:
            if titulo == None or len(titulo) <0 or titulo == '':
                pass
            else:
                try:
                    info_local = self.gerando_informacoes_candidatura[self.login]
                    info_local[0]=titulo
                    info_local[1]=Texto
                    self.gerando_informacoes_candidatura[self.login]=info_local
                except:
                    info_local=[]
                    info_local.append(titulo)
                    info_local.append(Texto)
                    self.gerando_informacoes_candidatura[self.login]=info_local

        return self.gerando_informacoes_candidatura[self.login]

    def global_list(self,request):

        info = []

        for location in Election.objects.all().values():
            print(location)
            usuario = Usuario.objects.get(Id_Academico = location['Usuario_id'])
            if location['Ativo'] == True:
                Ativo ='Ativo'
            else:
                Ativo ='Inativo'
            info.append([location['N_Eleicao'],usuario.Nome,location[ 'Titulo'],location['End_Data'],Ativo,'Link'])
            #print('\n\n\n\n',info)
        return info

    def global_list_urna(self,request,eleicao,qual_lista,modificar):
        try:
            self.limpar_memoria("apagar_lista_texto")
        except:
            pass
        try:
            self.limpar_memoria( "apagar_lista_candiatos")
        except:
            pass
        if self.login not in self.local_atual_eleicao:
            self.local_atual_eleicao[self.login]= ['','']
        info_local=[]
        if modificar == True:
            info_local = self.local_atual_eleicao[self.login]
            info_local[0]=eleicao
            info_local[1]=qual_lista
            self.local_atual_eleicao[self.login]=info_local


        return self.local_atual_eleicao[self.login]

    def lista_candidatos(self,request,lista_candidatos):
        print('\n\nxxx',lista_candidatos)
        eleicao = Election.objects.get(N_Eleicao = lista_candidatos)
        #eleicao = Election.values_list(N_Eleicao = lista_candidatos)
        eleitores = Data_Election.objects.filter(N_Eleicao = eleicao.pk).all()
        #print(dir(eleitores),'xxxxx\n\n\n')

        #print(dir(Election))
        #print(dir(x))
        info_see = []
        info_more =[]
        for info in eleitores.values():##Informando o Ultimo ID de todos elementos da Eleição
            print([info['N_Eleicao_id'],info['Candidatos'],info[ 'N_Candidato'],info['Votos']])
            info_more.append([info['N_Eleicao_id'],info['Candidatos'],info[ 'N_Candidato'],info['Votos']])
            if info['Candidatos'] != 'Null':
                info_see.append([info['Candidatos'],info[ 'N_Candidato']])
        print(info_see)
           
        #id_end =  int(re.sub('[^0-9]',' ', str(id_end)))
        return info_see,info_more