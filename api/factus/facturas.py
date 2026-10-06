import os
from decimal import Decimal, ROUND_HALF_UP

import requests

from .auth import obtener_token

IVA = Decimal("1.19")
CENTAVOS = Decimal("0.01")


def _dos_decimales(valor):
    return str(Decimal(valor).quantize(CENTAVOS, rounding=ROUND_HALF_UP))


def cliente_consumidor_final():
    return {
        "identification_document_code": "13",
        "identification": "22222222222",
        "names": "Consumidor Final",
        "legal_organization_code": "2",
        "tribute_code": "ZZ",
    }


def construir_items(transaccion):
    items = []
    for detalle in transaccion.detalles.select_related("producto"):
        precio_sin_iva = Decimal(detalle.precio) / IVA
        items.append(
            {
                "code_reference": f"PROD-{detalle.producto_id}",
                "name": detalle.producto.nombre,
                "quantity": _dos_decimales(detalle.cantidad),
                "discount_rate": "0.00",
                "price": _dos_decimales(precio_sin_iva),
                "unit_measure_code": "94",
                "standard_code": "999",
                "taxes": [{"code": "01", "rate": "19.00"}],
            }
        )
    return items


def construir_payload(transaccion):
    return {
        "reference_code": transaccion.referencia,
        "document": "01",
        "numbering_range_id": int(os.getenv("FACTUS_RANGO_ID")),
        "operation_type": "10",
        "send_email": False,
        "payment_details": [
            {
                "payment_form": "1",
                "payment_method_code": "42",
                "reference_code": transaccion.referencia,
                "amount": _dos_decimales(transaccion.monto),
            }
        ],
        "customer": cliente_consumidor_final(),
        "items": construir_items(transaccion),
    }


def crear_factura(transaccion):
    respuesta = requests.post(
        f"{os.getenv('FACTUS_URL')}/v2/bills/validate",
        json=construir_payload(transaccion),
        headers={
            "Authorization": f"Bearer {obtener_token()}",
            "Accept": "application/json",
        },
        timeout=60,
    )

    if respuesta.status_code not in (200, 201):
        raise Exception(
            f"Error creando factura en Factus ({respuesta.status_code}): {respuesta.text}"
        )

    return respuesta.json()["data"]["number"]


import base64


def descargar_pdf(numero_factura):
    respuesta = requests.get(
        f"{os.getenv('FACTUS_URL')}/v2/bills/{numero_factura}/download-pdf",
        headers={
            "Authorization": f"Bearer {obtener_token()}",
            "Accept": "application/json",
        },
        timeout=60,
    )

    if respuesta.status_code != 200:
        raise Exception(
            f"Error descargando PDF ({respuesta.status_code}): {respuesta.text}"
        )

    datos = respuesta.json()["data"]
    contenido = base64.b64decode(datos["pdf_base_64_encoded"])
    nombre = datos.get("file_name") or f"{numero_factura}.pdf"
    if not nombre.lower().endswith(".pdf"):
        nombre += ".pdf"
    return contenido, nombre
