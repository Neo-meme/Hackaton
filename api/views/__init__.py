from .admin_panel import (
    compras_admin,
    crear_producto,
    editar_producto,
    eliminar_producto,
    productos_admin,
)
from .auth import cerrar_sesion, index, login_view
from .cart import (
    agregar_carrito,
    aumentar_carrito,
    carrito,
    disminuir_carrito,
)
from .catalogo import productos
from .compras import factura_pdf, mis_compras
from .pagos import checkout, verificar_pago