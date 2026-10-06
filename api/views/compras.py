import logging

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from api.factus.facturas import descargar_pdf
from api.models import Transaccion

logger = logging.getLogger(__name__)


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