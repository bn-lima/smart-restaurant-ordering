from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .services import MercadoPagoClient, create_payload
from cart.services import get_cart

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