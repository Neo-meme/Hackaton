from django.db import models
from django.contrib.auth.models import User

# No se crea tabla de usuarios, se usa la predeterminada de Django

# Guarda los productos que vamos a mostrar en la tienda
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="productos/", blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# Guarda lo que el usuario va agregando al carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"


# Guarda cada compra y el estado del pago y la factura
class Transaccion(models.Model):
    ESTADOS_PAGO = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("cancelado", "Cancelado"),
    ]

    ESTADOS_FACTURA = [
        ("pendiente", "Pendiente"),
        ("generada", "Generada"),
        ("error", "Error"),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    referencia = models.CharField(max_length=100, unique=True)
    estado_pago = models.CharField(
        max_length=20,
        choices=ESTADOS_PAGO,
        default="pendiente"
    )
    estado_factura = models.CharField(
        max_length=20,
        choices=ESTADOS_FACTURA,
        default="pendiente"
    )
    numero_factura = models.CharField(max_length=100, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.referencia


class DetalleTransaccion(models.Model):
    transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.PositiveIntegerField()

    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"
    