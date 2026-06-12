import requests
from django.conf import settings
import hmac
import hashlib

class MercadoPagoClient():  # classe cliente pra fazer requisições HTTP pro Mercado Pago
    BASE_DIR = "https://api.mercadopago.com/"  # url base da API 

    def __init__(self):
        self.access_token = settings.MP_ACCESS_TOKEN  # token de acesso vindo das configs do Django

    def request(self, method, endpoint, data=None):
        response = requests.request(  # faz requisição HTTP genérica
            method,
            f"{self.BASE_DIR}{endpoint}",  # monta url completa
            headers={
                "Authorization": f"Bearer {self.access_token}",  # autenticação na API
                "Content-Type": "application/json"  # define envio em JSON
            },
            json=data  # corpo da requisição
        )

        response.raise_for_status()  # levanta erro se request falhar
        return response # retorna resposta convertida em json


def create_payload(cart, device):  # monta payload da ordem pra maquininha

    return {
        "type": "point",  # define que é pagamento via maquininha
        "external_reference": f"Cart #{cart.id}",  # id do pedido no sistema
        "transactions": {
            "payments": [
                {
                    "amount": str(cart.get_total())  # valor total do carrinho
                }
            ]
        },
        "config": {
            "point": {
                "terminal_id": str(device.point_terminal_id)  # id da maquininha destino
            }
        }
    }

def get_signature(x_signature):

    ts = None
    v1 = None

    for part in x_signature.split(","):

        key, value = part.split("=")

        if key == "ts":
            ts = value

        elif key == "v1":
            v1 = value

    if not ts or not v1:
        return None, None

    return ts, v1

def validate_signature(ts, v1, x_request_id, order_id):

    manifest = (
        f"id:{order_id};"
        f"request-id:{x_request_id};"
        f"ts:{ts};"
    )

    generated_hash = hmac.new(
        settings.MP_WEBHOOK_SECRET.encode(),
        manifest.encode(),
        hashlib.sha256           
    ).hexdigest()

    if not hmac.compare_digest(generated_hash, v1):
        return False
    return True