from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Sum, Min
from django.contrib.auth.models import User,AnonymousUser
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import FormUser,FormLogin,FormImagem,Formulario_part1,Formulario_part2,Formularios_Para_Votar,Select_day
from Users.models import User as Usuario
from Users.models import Election,Data_Election,Interaction_User,Activity_Report
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

        username = request.POST.get('Id_Academico')
        Nome = request.POST.get('Nome')
        email = request.POST.get('email') 
        password = request.POST.get('Senha')
        Cpf = request.POST.get('CPF')
        Genero = request.POST.get('Genero')
        if request.method == 'POST':
            #form = FormUser(request.POST)
            user = User.objects.create_user(username=username, email=email, password=password)
            form1 = Usuario(username,Nome,Cpf,Genero,email,user.password,None)
            '''for eleitor,n_eleitoral in zip(lista_candidatos,lista_numero):
                formulario_aprofundado_eleicao= Data_Election(N_Eleicao = formulario_eleicao,Candidatos=eleitor,N_Candidato = n_eleitoral,Votos=0)    
                formulario_aprofundado_eleicao.save()'''
            user.save()
            form1.save()
            messages.success(request,"Conta Criada com Sucesso")
            return redirect('login')
        else: 
            messages.success(request,"Erro de Autenticação no Formulário")
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
                return redirect('home')
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
        #
        newinfo=ações_Usuarios(str(request.user),'sim').pagination_list(request,info,False,False,False,False)

        #
        enviar_para_Urna = Formularios_Para_Votar(request.POST)
        if request.POST.get('local_urna') != None:
            return redirect('Urna')
            aux = ações_Usuarios(str(request.user),'sim').global_list_urna(request,aux2,'Lista_Eleicoes',True)
        
        #print(aux2)        
        if request.method == 'GET':
            
            return render(request,"lista_eleicoes.html",{'x':False,'TheList':newinfo,'Urna':enviar_para_Urna})

        return redirect('Urna')
        if request.method =='POST':
            aux2 = request.POST.get('local_urna')
            if aux2 !=None:
                #print(aux,aux2)
                ações_Usuarios(str(request.user),'sim').global_list_urna(request,aux2,'lista_eleicoes',True)
                Urna(request)
        return render(request,"lista_eleicoes.html",{'x':False,'TheList':newinfo,'Urna':enviar_para_Urna})
    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        info = ações_Usuarios(str(request.user),'sim').global_list(request)
        newinfo=ações_Usuarios(str(request.user),'sim').pagination_list(request,info,False,False,False,False)
        enviar_para_Urna = Formularios_Para_Votar(request.POST)
        #print(info)
        #print(enviar_para_Urna)
       
        if request.method == 'GET':

            return render(request,"lista_eleicoes.html",{'x':True,'usuario_logado':usuario_logado,'TheList':info[0:5],'Urna':enviar_para_Urna})
        
            
        if request.method =='POST':

            
            if request.POST.get('local_urna') != None:
                x = request.POST.get('local_urna')
                print(request.POST.get('Fim'))
                ações_Usuarios(str(request.user),'sim').global_list_urna(request,x,'lista_eleicoes',True)
                return redirect('Urna')
            if request.POST.get('Inicio') != None:
                newinfo=ações_Usuarios(str(request.user),'sim').pagination_list(request,info,True,False,False,False)
                print(info)
            elif request.POST.get('Anterior') != None:
                newinfo=ações_Usuarios(str(request.user),'sim').pagination_list(request,info,False,True,False,False)
                print(info)
            elif request.POST.get('Proximo') != None:
                newinfo=ações_Usuarios(str(request.user),'sim').pagination_list(request,info,False,False,True,False)
                print(info) 
            elif request.POST.get('Fim') != None:
                newinfo=ações_Usuarios(str(request.user),'sim').pagination_list(request,info,False,False,False,True)
                print(info)
            return render(request,"lista_eleicoes.html",{'x':True,'usuario_logado':usuario_logado,'TheList':newinfo,'Urna':enviar_para_Urna})
            
        return render(request,"lista_eleicoes.html",{'x':True,'usuario_logado':usuario_logado,'TheList':newinfo,'Urna':enviar_para_Urna})
 



def Urna(request):
    x =str(request.user) == 'AnonymousUser'
    if x:
        return render(request,"Urna.html",{'x':False})
    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))

        formularios = Formularios_Para_Votar(request.POST)
        info_Rapida = ações_Usuarios(str(request.user),'sim').global_list_urna(request,'','',False)
        info_candidatos,info_aprofundado = ações_Usuarios(str(request.user),info_Rapida[1]).lista_candidatos(request,info_Rapida[0])
        info_eleicao = Election.objects.get(N_Eleicao = info_Rapida[0])
        vencedor= []
        aux = 0
        for x in info_aprofundado:
            if x[0] != 'Null':
                if x[1] > aux:
                    vencedor = [x]
                elif x[1] == aux and aux != 0:
                    vencedor.append(x)


        print(vencedor,'\n\n\n\n\n')
        try:
            if request.method =='GET':
                return render(request,"Urna.html",{'x':True,'candidatos':info_candidatos,'candidatosend':info_aprofundado,'Eleitoral':info_eleicao,'result':vencedor,'formularios':formularios,'usuario_logado':usuario_logado})
            return render(request,"Urna.html",{'x':True,'candidatos':info_candidatos,'candidatosend':info_aprofundado,'Eleitoral':info_eleicao,'result':vencedor,'usuario_logado':usuario_logado})
                
        except:
            #print(formularios.Form1)
            return render(request,"Urna.html",{'x':True,'candidatos':info_candidatos,'candidatosend':info_aprofundado,'Eleitoral':info_eleicao,'result':vencedor,'formularios':formularios,'usuario_logado':usuario_logado})




def votar(request):
    if str(request.user) == 'anonymousUser':
        return render(request,"votar.html")
    usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
    info_Rapida = ações_Usuarios(str(request.user),'sim').global_list_urna(request,'','',False)
    info_eleicao = Election.objects.get(N_Eleicao = info_Rapida[0])
    interacao_usuario = Interaction_User.objects.all().filter(Usuario = usuario_logado,N_Eleicao =info_eleicao).values_list()  
    info_candidatos,info_candidatos_profundo = ações_Usuarios(str(request.user),info_Rapida[1]).lista_candidatos(request,info_Rapida[0])

    if len(interacao_usuario) > 0:
        print('achado!!!!!')
        messages.success(request,f"Você Não pode Participar duas vezes")
        return redirect('Urna')
    else:
        if request.method == 'GET':

            info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'',False,False)
            print(info) 
            return render(request,"votar.html",{'x':True,'usuario_logado':usuario_logado,'Eleitoral':info_eleicao,'lcd_vote':info}) 
        if request.method == 'POST':

            if request.POST.get('b0') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'0',True,False)
                print(info)
            elif request.POST.get('b1') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'1',True,False)
                print(info)
            elif request.POST.get('b2') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'2',True,False)
                print(info)
            elif request.POST.get('b3') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'3',True,False)
                print(info)
            elif request.POST.get('b4') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'4',True,False)
                print(info)
            elif request.POST.get('b5') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'5',True,False)
                print(info)
            elif request.POST.get('b6') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'6',True,False)
                print(info)
            elif request.POST.get('b7') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'7',True,False)
                print(info)
            elif request.POST.get('b8') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'8',True,False)
                print(info)
            elif request.POST.get('b9') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'9',True,False)
                print(info)
            elif request.POST.get('Null') != None:
                print('Null')
            elif request.POST.get('Cancelar') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'0',False,True)
            elif request.POST.get('Votar') != None:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'0',False,False)
                info_candidatos,info_candidatos_profundo = ações_Usuarios(str(request.user),info_Rapida[1]).lista_candidatos(request,info_Rapida[0])
                #eleitores = Data_Election.objects.filter(N_Eleicao = eleicao.pk).all()
                ballon = False
                for verificando in info_candidatos_profundo:
                    print(verificando)
                    if verificando[2] != 0:
                        if str(info) == str(verificando[2]):
                            voto = Data_Election.objects.filter(N_Eleicao = info_Rapida[0]).get(N_Candidato = info)
                            voto.Votos+=1
                            voto.save()
                            usuario = Usuario.objects.get(Id_Academico = request.user)
                            #Eleicao = Election.objects.get(N_eleicao = info_Rapida[0])
                            eleitor=Interaction_User(Usuario = usuario,N_Eleicao =info_eleicao,Data = datetime.datetime.now())
                            eleitor.save()
                            ballon =True
                        else:
                            print("nada")
                if ballon:
                    messages.success(request,f" Voto Efetuado com sucesso com sucesso!")
                    return redirect('Urna')
                else:
                    messages.success(request,f" Nem um Candidato foi encontrado...")
            try:
                info = ações_Usuarios(str(request.user),'sim').Seu_Voto(request,'0',False,False)
                print(info)
            except:
                pass
            return render(request,"votar.html",{'x':True,'usuario_logado':usuario_logado,'Eleitoral':info_eleicao,'lcd_vote':info,'lcd_candidato':info_candidatos}) 
        return render(request,"votar.html",{'x':True,'usuario_logado':usuario_logado,'Eleitoral':info_eleicao,'lcd_candidato':info_candidatos}) 


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
        print(titulo,'\n\n\n,')
        descricao = request.POST.get('Formulario2')
        lista_informacoes = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info2(request,titulo,descricao,True)
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
                titulo = request.POST.get('Formulario1')
                descricao = request.POST.get('Formulario2')
                try:
                    if len(titulo) <0 or len(descricao) <0:
                        titulo = lista_informacoes[0]
                        descricao=lista_informacoes[1]
                except:#problemas com nonetype
                        titulo = lista_informacoes[0]
                        descricao=lista_informacoes[1]
                lista_informacoes = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info2(request,titulo,descricao,False)
                lista_candidatos = ações_Usuarios(usuario_logado.Id_Academico,'sim').global_info(request,'',[],True,False)

                dias = datetime.timedelta(int(request.POST.get('select_day')))
                data = datetime.datetime.now()
                
                print(titulo)

                
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
        name = request.POST.get('Nome')
        print(name,name,'\n\n\n\n\n')
        if request.method == 'GET':
            return render(request,'suport_site.html',{'x': False})
        if request.method == 'POST':

            return render(request,'suport_site.html',{'x': False})

    else:
        usuario_logado= Usuario.objects.get(Id_Academico = str(request.user))
        name = request.POST.get('Nome')
        if request.method== 'GET':


            return render(request,"suport_site.html",{'x':True,'usuario_logado':usuario_logado})
        if request.method == 'POST':
            Nome = request.POST.get('Nome')
            if Nome != None:
                Sobrenome = request.POST.get('Sobrenome')
                if Sobrenome != None:
                    Email = request.POST.get('Email')
                    if Email != None:
                        Problem = request.POST.get('Problem')
                    if Problem != None:
                        Texto = request.POST.get('texto')
                        if Texto != None:

                            Formulario = Activity_Report(nome= Nome, sobrenome = Sobrenome, email = Email,titulo = Problem,balao =Texto)
                            Formulario.save()
                            messages.success(request,"Formulário enviado com Sucesso")
                            return render(request,"suport_site.html",{'x':True,'usuario_logado':usuario_logado})
            else:   
                messages.success(request,"Erro de autenticação")
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
    pagination={}
    Voto ={}
    def __init__(self,login,pagina_atual):
        global gerando_lista_candidatos
        global gerando_informacoes_candidatura
        global local_atual_eleicao
        global pagination
        global Voto
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
                    if self.login in self.Voto:
                        self.Voto.pop(self.login)
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
            if self.login in self.Voto:
                self.Voto.pop(self.login)
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
            usuario = Usuario.objects.get(Id_Academico = location['Usuario_id'])

            date= location['End_Data']

            date = str(date).split('-')
                
            date_end=datetime.date(int(date[0]),int(date[1]),int(date[2]))

            if date_end > datetime.datetime.now().date():
                Ativo ='Ativo'
                
            else:
                Ativo= 'Inativo'
                if location['Ativo'] == True:
                    info2 = Election.objects.get(N_Eleicao = location['N_Eleicao'])
                    info2.Ativo= 0
                    info2.save()
            info.append([location['N_Eleicao'],usuario.Nome,location[ 'Titulo'],location['End_Data'],Ativo,'Link'])
            #print('\n\n\n\n',info)
        return info

    def pagination_list(self,request,info,Inicio,Anterior,Proximo,Fim):
        cont=0
        if len(info)>=0:
            for linha in info:
                cont+=1
            print(cont)
            if self.login == "AnonymousUser":
                if cont>=5:
                    return info[0:5]
                if cont<5:
                    return info[0:len(cont)]
            elif self.login not in self.pagination:
                # TABELA <> Inicio   <> Anterior <> proximo <> Fim
                if len(info)>=5:
                    self.pagination[self.login]=[0,5]
                    return info[0:5]
                else:
                    self.pagination[self.login]=[0,len(info)]
                    return info[0:len(info)]
                                          
            else:

                info_local= self.pagination[self.login]
                print(len(info))
                if len(info)<5:
                    print(len(info))
                    return info[0:len(info)-1]
                else:
                    print(info_local)
                    if Inicio == True:#inicio
                        if cont>=5:
                            info_local[0]=0
                            info_local[1]=5
                            self.pagination[self.login]=info_local
                            return info[0:5]
                        if cont<5:##inicio quebrado
                            info_local[0]=0
                            info_local[1]=len(cont)
                            self.pagination[self.login]=info_local
                            return info[0:len(cont)]
                    elif Anterior == True:#anterior
                        if info_local[0]-5 >=0:
                            info_local[0]-=5
                            info_local[1]-=5
                            if info_local[0]<0:
                                info_local[0]=0
                                info_local[1]=5
                            self.pagination[self.login]=info_local
                            return info[info_local[0]:info_local[1]]
                        else:#anterior caso deça a casa 5 limitar
                            info_local[0]=0
                            info_local[1]=5
                            self.pagination[self.login]=info_local
                            return info[info_local[0]:info_local[1]]      
                    elif Fim == True:
                        if cont%5==0:
                            info_local[0]=cont-5
                            info_local[1]=cont
                            self.pagination[self.login]=info_local
                        else:
                            
                            end_cont = cont%5
                            cont= cont -end_cont
                            info_local[0]=cont
                            info_local[1]=cont+end_cont
                        self.pagination[self.login]=info_local
                        return info[info_local[0]:info_local[1]]
                    elif Proximo == True:
                        if cont%5==0:
                            if info_local[1]+5 <= cont:
                                info_local[0]+=5
                                info_local[1]+=5
                                self.pagination[self.login]=info_local
                                return info[info_local[0]:info_local[1]]
                        else:
                            
                            end_cont = cont%5
                            cont= cont -end_cont
                            info_local[0]=cont
                            info_local[1]=cont+end_cont
                        self.pagination[self.login]=info_local
                        return info[info_local[0]:info_local[1]]
                    '''else:

                        if Fim == True:
                            info_local[0]=cont
                            info_local[1]=end_cont+cont  
                            self.pagination[self.login]=info_local                      
                            return info[info_local[0]:info_local[1]]
                        elif Proximo == True:
                            if info_local[1]+5 <= cont:
                                info_local[0]+=5
                                info_local[1]+=5
                                if info_local[0]>cont:
                                    info_local[0]=cont-5
                                    info_local[1]=cont
                                self.pagination[self.login]=info_local
                                return info[info_local[0]:info_local[1]]
                            else:
                                info_local[0]+=cont
                                info_local[1]+=end_cont+cont  
                                self.pagination[self.login]=info_local                      
                                return info[info_local[0]:info_local[1]]'''
                                
        else:
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
        eleicao = Election.objects.get(N_Eleicao = lista_candidatos)
        #eleicao = Election.values_list(N_Eleicao = lista_candidatos)
        eleitores = Data_Election.objects.filter(N_Eleicao = eleicao.pk).all()
        #print(dir(eleitores),'xxxxx\n\n\n')
        cont= Data_Election.objects.filter(N_Eleicao_id = eleicao.pk).aggregate(Sum('Votos'))
        print(cont)
        #print(dir(Election))
        #print(dir(x))
        info_see = []
        info_more =[]
        for info in eleitores.values():##Informando o Ultimo ID de todos elementos da Eleição
            try:
                info_more.append([info['Candidatos'],info['Votos'],str(int((info['Votos'])/int(cont['Votos__sum']))*100)+'%'])
            except:
                info_more.append([info['Candidatos'],info['Votos'],str(int(0))+'%'])
            if info['Candidatos'] != 'Null':
                info_see.append([info['Candidatos'],info[ 'N_Candidato']])
        #print(info_see)
           
        #id_end =  int(re.sub('[^0-9]',' ', str(id_end)))
        return info_see,info_more

    def Seu_Voto(self,request,botao,modificar,apagar):
        if self.login not in self.Voto:
            self.Voto[self.login]=''

        if apagar == True:
            if self.login in self.Voto:
                self.Voto.pop(self.login)
                return ''
        else:
            if modificar == True:
                if self.login in self.gerando_lista_candidatos:
                    self.gerando_lista_candidatos.pop(self.login)
                if self.login in self.gerando_informacoes_candidatura:
                    self.gerando_informacoes_candidatura.pop(self.login)
                try:
                    if len(self.Voto[self.login])<5:
                        self.Voto[self.login]+=botao
                except:

                    self.Voto[self.login]=botao

        return self.Voto[self.login]