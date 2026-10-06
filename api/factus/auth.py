import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

_token = None
_expira_en = 0
MARGEN_SEGUNDOS = 30


def obtener_token():
    global _token, _expira_en

    if _token and time.time() < _expira_en - MARGEN_SEGUNDOS:
        return _token

    respuesta = requests.post(
        f"{os.getenv('FACTUS_URL')}/oauth/token",
        data={
            "grant_type": "password",
            "client_id": os.getenv("FACTUS_CLIENT_ID"),
            "client_secret": os.getenv("FACTUS_CLIENT_SECRET"),
            "username": os.getenv("FACTUS_USERNAME"),
            "password": os.getenv("FACTUS_PASSWORD"),
        },
        headers={"Accept": "application/json"},
        timeout=15,
    )

    if respuesta.status_code != 200:
        raise Exception(
            f"Error autenticando en Factus API ({respuesta.status_code}): {respuesta.text}"
        )

    datos = respuesta.json()
    _token = datos["access_token"]
    _expira_en = time.time() + int(datos.get("expires_in", 0))

    return _token