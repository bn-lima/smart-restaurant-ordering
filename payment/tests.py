from rest_framework.test import APITestCase
from unittest.mock import patch
from devices.models import Device
from cart.models import CartItem
from restaurant_menu.models import MenuItem
from cart.services import get_cart
from django.urls import reverse
class MockMercadoPago(APITestCase): # classe de testes do pagamento

    def setUp(self):
        
        self.device = Device.objects.create( # cria dispositivo fake
            username="fake_device",
            function="Checkout",
            point_terminal_id="fake_hash"
        )

        self.device.set_password("12345678") # define senha do dispositivo
        self.device.save() # salva dispositivo

        self.menu_item = MenuItem.objects.create( # cria item do cardápio
            item_name="Lasanha",
            item_description="Lasanha à bolonhesa",
            item_ingredients="Massa, queijo, molho",
            item_price="29.90",
            active=True,
            item_category="Sobremesas"
        )

        self.cart, _ = get_cart(self.device) # obtém carrinho do dispositivo

        self.cart_item = CartItem.objects.create(cart=self.cart, quantity=2, menu_item=self.menu_item) # adiciona item ao carrinho

        self.webhook_query_params = "data.id=ord_test_001" # Query string recebida no webhook
        
        self.webhook_json = { # Payload enviado pelo Mercado Pago
            "action": "order.processed",
            "api_version": "v1",
            "type": "order",
            "data": {
                "id": "ord_test_001",
                "external_reference": "Cart #1"
            }
        }

    @patch("payment.views.MercadoPagoClient.request")
    def test_mercado_pago_request(self, mock_mercado_pago_request):

        url = reverse("payment") # Endpoint responsável por criar o pagamento

        self.client.force_authenticate(user=self.device) # autentica dispositivo

        mock_mercado_pago_request.return_value.status_code = 201 # simula sucesso HTTP

        mock_mercado_pago_request.return_value.json.return_value = { # simula resposta da API
            "id": "ORD_TEST",
            "status": "created"
        }

        response = self.client.post(url, format="json") # envia requisição POST

        mock_mercado_pago_request.assert_called_once() # verifica se requisição foi chamada

        self.assertEqual(response.status_code, 201) # valida status da resposta

        self.assertEqual(response.data["id"], "ORD_TEST") # valida id retornado

        print(response.data, response.status_code)

    @patch("payment.views.validate_signature") # Mock da validação criptográfica da assinatura
    @patch("payment.views.get_signature") # Mock da extração dos dados da assinatura
    def test_webhook(self, mock_get_signature, mock_validate_signature):

        url = reverse("webhook") # Endpoint de recebimento de eventos
 
        mock_get_signature.return_value = (True, True) # Simula assinatura presente e válida

        mock_validate_signature.return_value = True # Simula validação bem sucedida

        response = self.client.post(
            url,
            data=self.webhook_json,
            format="json",
            HTTP_X_SIGNATURE="ts=1749500000,v1=12345678910",
            HTTP_X_REQUEST_ID="test-request-123",
            QUERY_STRING=self.webhook_query_params
        )

        mock_get_signature.assert_called_once() # Verifica extração da assinatura
        mock_validate_signature.assert_called_once() # Verifica validação da assinatura

        self.assertEqual(response.status_code, 200) # Webhook processado com sucesso