import os
import requests
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


def autenticar():
    url = "https://pay-api-sandbox.factus.com.co/auth"

    datos = {
        "email": os.getenv("FACTUS_PAY_EMAIL"),
        "password": os.getenv("FACTUS_PAY_PASSWORD")
    }

    respuesta = requests.post(
        url,
        json=datos,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )

    print("STATUS AUTENTICACIÓN:", respuesta.status_code)
    print("RESPUESTA AUTENTICACIÓN:", respuesta.text)

    respuesta.raise_for_status()

    datos_respuesta = respuesta.json()

    if "token" not in datos_respuesta:
        raise Exception(
            f"Factus Pay no devolvió un token: {datos_respuesta}"
        )

    return datos_respuesta["token"]


def crear_recaudo(referencia, monto):
    token = autenticar()

    url = "https://pay-api-sandbox.factus.com.co/v1/collections"

    datos = {
        "reference_code": referencia,
        "amount": int(monto)
    }

    respuesta = requests.post(
        url,
        json=datos,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    )

    print("STATUS CREAR RECAUDO:", respuesta.status_code)
    print("RESPUESTA CREAR RECAUDO:", respuesta.text)

    respuesta.raise_for_status()

    return respuesta.json()


def consultar_recaudo(referencia):
    token = autenticar()

    url = f"https://pay-api-sandbox.factus.com.co/v1/collections/{referencia}"

    respuesta = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    )

    print("STATUS CONSULTAR RECAUDO:", respuesta.status_code)
    print("RESPUESTA CONSULTAR RECAUDO:", respuesta.text)

    respuesta.raise_for_status()

    return respuesta.json()
