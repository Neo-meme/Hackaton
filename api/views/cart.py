from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from api.models import Carrito, Producto


@login_required
def agregar_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)

    carrito = Carrito.objects.filter(
        usuario=request.user,
        producto=producto
    ).first()

    if carrito:
        carrito.cantidad += 1
        carrito.save()
    else:
        Carrito.objects.create(
            usuario=request.user,
            producto=producto,
            cantidad=1
        )

    return redirect("productos")


@login_required
def carrito(request):
    productos_carrito = Carrito.objects.filter(
        usuario=request.user
    )

    total = 0

    for item in productos_carrito:
        item.subtotal = item.producto.precio * item.cantidad
        total += item.subtotal

    return render(
        request,
        "carrito.html",
        {
            "productos_carrito": productos_carrito,
            "total": total
        }
    )


@login_required
def aumentar_carrito(request, id):
    item = get_object_or_404(
        Carrito,
        id=id,
        usuario=request.user
    )

    item.cantidad += 1
    item.save()

    return redirect("carrito")


@login_required
def disminuir_carrito(request, id):
    item = get_object_or_404(
        Carrito,
        id=id,
        usuario=request.user
    )

    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()

    return redirect("carrito")