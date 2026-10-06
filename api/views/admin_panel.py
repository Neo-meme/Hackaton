from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from api.models import Producto, Transaccion


def es_admin(usuario):
    return usuario.is_staff


@login_required
@user_passes_test(es_admin)
def productos_admin(request):
    productos = Producto.objects.all()

    return render(
        request,
        "admin_productos.html",
        {"productos": productos}
    )


@login_required
@user_passes_test(es_admin)
def crear_producto(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        precio = request.POST["precio"]
        descripcion = request.POST["descripcion"]
        imagen = request.FILES.get("imagen")

        Producto.objects.create(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            imagen=imagen
        )

        return redirect("productos_admin")

    return render(request, "crear_producto.html")


@login_required
@user_passes_test(es_admin)
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        producto.nombre = request.POST["nombre"]
        producto.precio = request.POST["precio"]
        producto.descripcion = request.POST["descripcion"]

        if request.FILES.get("imagen"):
            producto.imagen = request.FILES.get("imagen")

        producto.save()

        return redirect("productos_admin")

    return render(
        request,
        "editar_producto.html",
        {"producto": producto}
    )


@login_required
@user_passes_test(es_admin)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        producto.delete()

    return redirect("productos_admin")


@login_required
@user_passes_test(es_admin)
def compras_admin(request):
    compras = Transaccion.objects.select_related(
        "usuario"
    ).order_by("-fecha")

    return render(
        request,
        "admin_compras.html",
        {"compras": compras}
    )