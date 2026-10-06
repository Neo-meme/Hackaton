from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Producto
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito
from .models import Producto, Carrito, Transaccion, DetalleTransaccion
from .factuspay import crear_recaudo, consultar_recaudo
from .factus.facturas import crear_factura
from django.http import Http404, HttpResponse
from api.factus.facturas import descargar_pdf

def index(request):
    return redirect("login")


def es_admin(usuario):
    return usuario.is_staff


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

@login_required
def productos(request):

    productos = Producto.objects.filter(activo=True)

    return render(
        request,
        "productos.html",
        {"productos": productos}
    )


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

def cerrar_sesion(request):
    logout(request)
    return redirect("login")

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



@login_required
def checkout(request):

    productos_carrito = Carrito.objects.filter(
        usuario=request.user
    )

    if not productos_carrito.exists():
        return redirect("carrito")

    total = 0

    for item in productos_carrito:
        total += item.producto.precio * item.cantidad

    referencia = f"COMPRA-{request.user.id}-{Transaccion.objects.count() + 1}"

    transaccion = Transaccion.objects.create(
        usuario=request.user,
        monto=total,
        referencia=referencia
    )

    for item in productos_carrito:

        DetalleTransaccion.objects.create(
            transaccion=transaccion,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )

    resultado = crear_recaudo(
        transaccion.referencia,
        transaccion.monto
    )

    qr = resultado["data"]["qr"]

    productos_carrito.delete()

    return render(
        request,
        "checkout.html",
        {
            "transaccion": transaccion,
            "resultado": resultado,
            "qr": qr
        }
    )


import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404, render

from api.factus.facturas import crear_factura
from api.models import Transaccion
# from api.xxx import consultar_recaudo   # deja tu import actual de consultar_recaudo

logger = logging.getLogger(__name__)



@login_required
def verificar_pago(request, id):
    if request.user.is_staff:
        transaccion = get_object_or_404(
            Transaccion,
            id=id
        )
    else:
        transaccion = get_object_or_404(
            Transaccion,
            id=id,
            usuario=request.user
        )

    resultado = consultar_recaudo(transaccion.referencia)
    estado = resultado["data"]["status"]

    if estado == "paid":
        with db_transaction.atomic():
            transaccion = Transaccion.objects.select_for_update().get(
                pk=transaccion.pk
            )

            transaccion.estado_pago = "pagado"

            if transaccion.estado_factura in ("pendiente", "error"):
                try:
                    numero_factura = crear_factura(transaccion)

                    transaccion.numero_factura = numero_factura
                    transaccion.estado_factura = "generada"

                    logger.info(
                        "Factura generada: %s",
                        numero_factura
                    )

                except Exception:
                    logger.exception(
                        "Error al generar factura Factus (transaccion %s)",
                        transaccion.pk
                    )

                    transaccion.estado_factura = "error"

            transaccion.save()

    return render(
        request,
        "verificar_pago.html",
        {
            "transaccion": transaccion,
            "resultado": resultado
        }
    )

@login_required
def mis_compras(request):
    compras = Transaccion.objects.filter(
        usuario=request.user
    ).order_by("-fecha")

    return render(
        request,
        "mis_compras.html",
        {"compras": compras}
    )

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



@login_required
def factura_pdf(request, id):
    if request.user.is_staff:
        transaccion = get_object_or_404(
            Transaccion,
            id=id
        )
    else:
        transaccion = get_object_or_404(
            Transaccion,
            id=id,
            usuario=request.user
        )

    if transaccion.estado_factura != "generada" or not transaccion.numero_factura:
        raise Http404("La factura aún no está disponible")

    try:
        contenido, nombre = descargar_pdf(transaccion.numero_factura)
    except Exception:
        logger.exception(
            "Error descargando PDF de factura %s",
            transaccion.numero_factura
        )
        return HttpResponse(
            "No se pudo obtener la factura, intenta de nuevo.",
            status=502
        )

    respuesta = HttpResponse(
        contenido,
        content_type="application/pdf"
    )
    respuesta["Content-Disposition"] = f'inline; filename="{nombre}"'

    return respuesta