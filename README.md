# smart-restaurant-ordering

Backend Django para um protótipo de restaurante inteligente.
O sistema suporta registro e autenticação de dispositivos, gestão de menu, carrinho, pagamento via Mercado Pago e processamento de pedidos para a cozinha.

## Visão Geral

- Backend em Django 6 + Django REST Framework.
- Autenticação por token usando `rest_framework.authentication.TokenAuthentication`.
- Usuário customizado: `devices.Device`.
- Dispositivos têm função: `checkout` ou `kitchen`.
- API modular com apps: `devices`, `control_panel`, `restaurant_menu`, `cart`, `kitchen` e `payment`.

## Funcionalidades

- Registro e login de dispositivos.
- Atualização de função e senha do dispositivo autenticado.
- Gerenciamento de dispositivos e itens de menu via painel de controle admin.
- Lista e criação de itens de menu.
- Carrinho de compras para dispositivos autenticados.
- Integração com Mercado Pago para criar pedidos de pagamento.
- Recebimento de webhook do Mercado Pago para criar pedidos de cozinha quando o pagamento é confirmado.
- Listagem e marcação de pedidos como entregues pela cozinha.

## Estrutura do Projeto

- `smart_restaurant/` - configurações Django.
- `devices/` - autenticação de dispositivos e modelos de usuário.
- `control_panel/` - endpoints administrativos para dispositivos e menu.
- `restaurant_menu/` - catálogo de itens do menu.
- `cart/` - carrinho de compras do dispositivo.
- `kitchen/` - gerenciamento de pedidos de cozinha.
- `payment/` - integração com Mercado Pago e webhook.
- `Dockerfile` - imagem para rodar a API.
- `docker-compose.yml` - orquestra API e PostgreSQL.

## Tecnologias

- Python 3.12
- Django 6.0.5
- Django REST Framework 3.17.1
- PostgreSQL 16
- psycopg 3
- requests
- python-dotenv

## Endpoints Principais

### Root da API

- `POST /device/register/` - registra novo dispositivo.
- `POST /device/register/admin/` - cria superusuário com token de criação.
- `POST /device/login/` - faz login e retorna `login_token`.
- `PATCH /device/update/function/` - atualiza a função do dispositivo autenticado.
- `POST /device/update/password/` - altera a senha do dispositivo autenticado.

### Menu

- `GET /menu/` - lista itens ativos do menu.
- `POST /menu/item/create/` - cria um novo item de menu (apenas admin).
- `GET /menu/item/<pk>/detail/` - detalha item de menu ativo.

### Carrinho

- `GET /cart/detail/` - mostra o carrinho ativo do dispositivo autenticado.
- `POST /cart/item/<pk>/add/` - adiciona ou atualiza quantidade de item no carrinho.
- `DELETE /cart/item/<pk>/remove/` - remove ou diminui quantidade do item no carrinho.
- `POST /cart/cancel/` - cancela o carrinho ativo.

### Pagamento

- `POST /payment/payment/` - cria ordem de pagamento no Mercado Pago para o carrinho ativo.
- `POST /payment/webhook/` - recebe notificações do Mercado Pago e cria pedidos de cozinha.

### Cozinha

- `GET /kitchen/orders/` - lista pedidos não entregues (apenas para dispositivos `kitchen`).
- `PATCH /kitchen/order/<pk>/deliver/` - marca pedido como entregue.

### Painel de Controle/Admin

- `GET /control_panel/devices/` - lista todos os dispositivos (apenas admin).
- `POST /control_panel/device/create/` - cria dispositivo via admin.
- `PATCH /control_panel/device/<pk>/update/` - atualiza dispositivo específico.
- `PATCH /control_panel/item/<pk>/update/` - atualiza item do menu.
- `DELETE /control_panel/item/<pk>/delete/` - exclui item de menu (apenas admin).

## Autenticação

- As rotas que exigem autenticação usam `TokenAuthentication`.
- Envie o cabeçalho `Authorization: Token <login_token>`.

## Requisitos de Ambiente

O projeto requer as seguintes variáveis no arquivo `.env`:

- `POSTGRES_HOST`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `DEVICE_AUTHENTICATION_TOKEN`
- `DEVICE_LOGIN_TOKEN`
- `DEVICE_RESET_PASSWORD_TOKEN`
- `CREATE_SUPERUSER_TOKEN`
- `MP_ACCESS_TOKEN`
- `MP_WEBHOOK_SECRET`

## Execução com Docker

1. Crie um arquivo `.env` com as variáveis acima.
2. Execute:

```bash
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.

## Interface Admin Django

- A interface Django admin fica em `/admin/`.
- Crie um superusuário usando o endpoint `POST /device/register/admin/`.

## Observações

- `devices.Device` é o modelo de usuário personalizado usado em `AUTH_USER_MODEL`.
- O fluxo de pagamento foi iniciado via Mercado Pago, usando `payment` para criar ordens e `webhook` para confirmação.
- A API contém suporte básico para menu, carrinho e pedidos, mas não inclui frontend.
- Ao rodar com Docker, o container `api` aguarda o PostgreSQL ficar disponível antes de aplicar as migrations.
