from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .services import MercadoPagoClient, create_payload, validate_signature, get_signature
from cart.services import get_cart, get_cart_by_id
from kitchen.services import create_order, order_exists

class MPPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        device = request.user # pega dispositivo autenticado

        if device.function == "kitchen": # impede dispositivos da cozinha de iniciar pagamento
            return Response({"detail": "You do not have permission to access this endpoint"}, status=status.HTTP_403_FORBIDDEN)
        
        cart, _ = get_cart(device) # Pega carrinho ativo

        if not cart.items.all().exists(): # verifica se carrinho possui itens
            return Response({"detail": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = create_payload(cart, device) # monta payload para enviar ao Mercado Pago

        mp_client = MercadoPagoClient() # instancia cliente da API do Mercado Pago
        response = mp_client.request("POST", "v1/orders", data=payload) # envia requisição de pagamento

        return Response(response.json(), status=response.status_code) # retorna resposta da API
class WebHook(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        
        x_signature = request.headers.get("x-signature")
        x_request_id = request.headers.get("x-request-id")

        if not x_signature or not x_request_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        order_id = request.query_params.get("data.id", None)

        if not order_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        order_id = order_id.lower()
        
        ts, v1 = get_signature(x_signature)

        if not ts or not v1:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Valida a autenticidade da notificação recebida
        validated = validate_signature(ts, v1, x_request_id, order_id)

        if not validated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        external_reference = request.data.get("data", {}).get("external_reference")

        if external_reference:
            # Pega o carrinho associado à ordem processada
            cart_id = external_reference.split("#")[1]

            cart = get_cart_by_id(int(cart_id))

            if not order_exists(cart):  # Garante que a mesma ordem não gere mais de um pedido
                create_order(cart)

        return Response(status=status.HTTP_200_OK)