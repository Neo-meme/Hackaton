from django.urls import path
from .views import index, login_view, panel, productos, agregar_carrito, carrito, aumentar_carrito, disminuir_carrito, checkout, verificar_pago, productos_admin, crear_producto, editar_producto, eliminar_producto, cerrar_sesion

urlpatterns = [
    path("", index),
    path("login/", login_view, name="login"),
    path("panel/", panel, name="panel"),
    path("productos/", productos, name="productos"),
    path("panel/productos/", productos_admin, name="productos_admin"),
    path("panel/productos/crear/", crear_producto, name="crear_producto"),
    path("logout/", cerrar_sesion, name="cerrar_sesion"),
    path("panel/productos/editar/<int:id>/", editar_producto, name="editar_producto"),
    path("panel/productos/eliminar/<int:id>/", eliminar_producto, name="eliminar_producto"),
    path("carrito/agregar/<int:id>/", agregar_carrito, name="agregar_carrito"),
    path("carrito/", carrito, name="carrito"),
    path("carrito/aumentar/<int:id>/", aumentar_carrito, name="aumentar_carrito"),
    path("carrito/disminuir/<int:id>/", disminuir_carrito, name="disminuir_carrito"),
    path("checkout/", checkout, name="checkout"),
    path("verificar-pago/<int:id>/", verificar_pago, name="verificar_pago"),
]