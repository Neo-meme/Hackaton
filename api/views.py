from django.http import JsonResponse
import requests


def prueba_http(request):
    respuesta = requests.get("https://httpbin.org/get")

    return JsonResponse({
        "status": respuesta.status_code,
        "respuesta": respuesta.json()
    })