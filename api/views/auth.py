from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def index(request):
    return redirect("login")


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("productos_admin")
        return redirect("productos")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)

            if usuario.is_staff:
                return redirect("productos_admin")

            return redirect("productos")

        return render(
            request,
            "login.html",
            {"error": "Usuario o contraseña incorrectos"}
        )

    return render(request, "login.html")


def cerrar_sesion(request):
    logout(request)
    return redirect("login")