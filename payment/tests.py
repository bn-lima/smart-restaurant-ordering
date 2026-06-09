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
        

    @patch("payment.views.MercadoPagoClient.request") # substitui requisição real por mock
    def test_mercado_pago_request(self, mock_mercado_pago_request):

        url = reverse("payment") # obtém url do endpoint

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

        print(response.data, response.status_code) # imprime resposta do teste