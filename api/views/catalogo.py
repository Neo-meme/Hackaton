from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from api.models import Producto


@login_required
def productos(request):
    productos = Producto.objects.filter(activo=True)

    return render(
        request,
        "productos.html",
        {"productos": productos}
    )