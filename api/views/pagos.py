import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404, redirect, render

from api.factus.facturas import crear_factura
from api.factuspay import consultar_recaudo, crear_recaudo
from api.models import Carrito, DetalleTransaccion, Transaccion

logger = logging.getLogger(__name__)


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

                    logger.info("Factura generada: %s", numero_factura)

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