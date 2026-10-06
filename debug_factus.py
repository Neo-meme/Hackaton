import json
import os

import requests

from api.models import Transaccion
from api.factus.facturas import construir_payload
from api.factus.auth import obtener_token

t = Transaccion.objects.get(id=8)
print("Transaccion:", t.id, t.referencia)

payload = construir_payload(t)
print(json.dumps(payload, indent=2, ensure_ascii=False))

r = requests.post(
    f"{os.getenv('FACTUS_URL')}/v2/bills/validate",
    json=payload,
    headers={
        "Authorization": f"Bearer {obtener_token()}",
        "Accept": "application/json",
    },
    timeout=60,
)
print("STATUS:", r.status_code)
print(r.text)
