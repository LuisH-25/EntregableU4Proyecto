from django.shortcuts import render, redirect, get_object_or_404   # redirect: me redirije segun el nombre que puse en urls, si se busca algo que no esta en la db sale error 404 y no tumbar el servidor

from django.http import HttpResponse            # Para enviar html basicos
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Para traer el template de signup(crear usuario y para comprobar si el usuario existe)
from django.contrib.auth.models import User     # para traer el modelo User
from django.contrib.auth import login, logout, authenticate           # para usar sesiones (abrir y cerrarla), authenticate: para comprobar el username
from django.db import IntegrityError            # marca errores de la db
from .forms import PortafolioForm
from .models import Portafolio,UsuarioIp
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ipware import get_client_ip

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        print("Enviando datos")
        return render(request, "signup.html", {
            "form": UserCreationForm})
    elif request.method == "POST":
        print(request.POST)
        print("Reciviendo datos")
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Registrar usuario
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                #login(request, user)
                return redirect("signin")  #return redirect("portafolios")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "El usuario ya existe"})

        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": "Las contrasenhas no coinciden"})

@login_required
def portafolios(request):
    #portafolios = Portafolio.objects.all()
    portafolios = Portafolio.objects.filter(user=request.user, datecompleted__isnull= True)
    return render(request, "portafolios.html", {"portafolios":portafolios, "estado":"pendientes"})

def portafolios_universal(request):
    portafolios = Portafolio.objects.filter(private = False)
    #portafolios = Portafolio.objects.filter(user=request.user, datecompleted__isnull= True)
    return render(request, "portafolios.html", {"portafolios":portafolios, "estado":"universales"})

@login_required
def portafolios_completed(request):
    #portafolios = Portafolio.objects.all()
    portafolios = Portafolio.objects.filter(user=request.user, datecompleted__isnull= False).order_by("-datecompleted")
    return render(request, "portafolios.html", {"portafolios":portafolios, "estado":"completados"})

@login_required
def create_portafolios(request):
    if request.method == "GET":
        return render(request,"create_portafolio.html",{
            "form": PortafolioForm
        })
    elif request.method == "POST":
        try:
            form = PortafolioForm(request.POST)
            new_portafolio = form.save(commit=False)
            new_portafolio.user = request.user
            print(new_portafolio)
            new_portafolio.save()
            return redirect("portafolios")
        except ValueError:
            return render(request,"create_portafolio.html",{
            "form": PortafolioForm,
            "error": "Ingrese datos validos"
            })

@login_required        
def portafolio_detail(request, portafolio_id):
    if request.method == "GET":
        print(portafolio_id)
        #portafolio = Portafolio.objects.get(pk=portafolio_id)
        portafolio = get_object_or_404(Portafolio, pk=portafolio_id, user= request.user)       # me aseguro que seo solo mis tareas. Si entro a otra tarea me da error 404
        form = PortafolioForm(instance=portafolio)  # El oformulario se rellena con los valores de "portafolio"
        return render(request, "portafolio_detail.html", {"portafolio" : portafolio, "form" : form})
    elif request.method == "POST":
        try:
            portafolio = get_object_or_404(Portafolio, pk=portafolio_id, user= request.user)
            form = PortafolioForm(request.POST, instance=portafolio)
            form.save()
            return redirect("portafolios")
        except ValueError:
            return render(request, "portafolio_detail.html", {"portafolio" : portafolio, "form" : form, "error": "Error actualizando la tarea"})

@login_required
def complete_portafolio(request, portafolio_id):
    portafolio = get_object_or_404(Portafolio, pk=portafolio_id, user= request.user)
    if request.method == "POST":
        portafolio.datecompleted = timezone.now()
        portafolio.save()
        return redirect("portafolios")

@login_required
def delete_portafolio(request, portafolio_id):
    portafolio = get_object_or_404(Portafolio,pk=portafolio_id, user= request.user)
    if request.method == "POST":
        portafolio.delete()
        return redirect("portafolios")


@login_required
def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    print(request.POST)
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm})
    elif request.method == "POST":
        user = authenticate(
            request, 
            username=request.POST["username"], 
            password=request.POST["password"])
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": "El usuario o contrasenha esta incorrecta"})
        else:
            login(request, user)
            ip, is_routable = get_client_ip(request)
            print("ip : "+ ip)
            usuarioIp = UsuarioIp.objects.create(ip_login = str(ip), user=user)
            usuarioIp.save()

            return redirect("portafolios")

