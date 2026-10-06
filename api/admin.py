from django.contrib import admin
from .models import Producto, Carrito, Transaccion


admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(Transaccion)