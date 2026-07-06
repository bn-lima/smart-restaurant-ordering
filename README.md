# smart-restaurant-ordering

Backend Django para um protótipo de restaurante inteligente.

Este repositório contém uma API REST modular para gerenciar dispositivos (clientes/terminais), catálogo de menu, carrinho de compras, integração com Mercado Pago e processamento de pedidos para a cozinha.

**Principais apps**

- `devices` — modelo de usuário customizado (`Device`) usado para representar terminais; endpoints para registro/login/atualização de função e senha; criação de superusuário via token.
- `restaurant_menu` — modelo `MenuItem`, listagem e detalhe dos itens do cardápio; busca por categoria.
- `cart` — gerenciamento do carrinho por dispositivo, adição/remoção de itens e cálculo de totais.
- `kitchen` — modelo `Order` e endpoints para listar/entregar pedidos (fluxo da cozinha).
- `payment` — integração com Mercado Pago: cria ordens e recebe webhooks para confirmar pagamentos e criar pedidos de cozinha.
- `control_panel` — endpoints administrativos para gerenciar dispositivos, itens do menu e visualizar pedidos.

## Requisitos

- Python 3.12
- PostgreSQL 16
- As dependências estão em `requirements.txt` (Django 6.0.5, DRF, python-dotenv, psycopg, Pillow, requests, etc.).

## Variáveis de ambiente (.env)

As variáveis esperadas pelo projeto:

- `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`, `POSTGRES_DB`
- `DEVICE_AUTHENTICATION_TOKEN` — UUID usado para validar o registro de dispositivos
- `DEVICE_LOGIN_TOKEN` — UUID usado para validar o login de dispositivos
- `DEVICE_RESET_PASSWORD_TOKEN` — UUID usado para reset de senha
- `CREATE_SUPERUSER_TOKEN` — UUID usado para criar superusuário via endpoint
- `MP_ACCESS_TOKEN`, `MP_WEBHOOK_SECRET` — credenciais do Mercado Pago

OBS: `smart_restaurant/settings.py` lê as variáveis via `python-dotenv`.

## Execução (Docker)

1. Crie um arquivo `.env` com as variáveis acima.
2. Build e up via Docker Compose:

```bash
docker compose up --build
```

A aplicação ficará acessível em `http://localhost:8000`.

O `Dockerfile` aguarda o serviço `db` (Postgres) ficar disponível antes de aplicar migrations e iniciar o servidor.

## Execução local sem Docker (opcional)

1. Crie e ative um virtualenv com Python 3.12.
2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Exporte as variáveis de ambiente ou crie um `.env` e use `python-dotenv`.
4. Rode migrations e inicie o servidor:

```bash
python manage.py migrate
python manage.py runserver
```

## Endpoints (rotas)

- Admin Django:
	- `GET /admin/` — painel administrativo do Django

- Dispositivos (`devices` — prefixo `/device/`):
	- `POST /device/register/` — registrar dispositivo (`RegisterDevice`)
	- `POST /device/register/admin/` — criar superusuário (`CreateAdminUser`)
	- `POST /device/login/` — login de dispositivo (`LoginDevice`)
	- `PATCH /device/update/function/` — alterar função do dispositivo autenticado (`UpdateDeviceFunction`)
	- `POST /device/update/password/` — alterar senha do dispositivo autenticado (`UpdateDevicePassword`)

- Painel de controle (`control_panel` — prefixo `/control_panel/`):
	- `GET /control_panel/devices/` — listar todos os dispositivos (`DevicesList`)
	- `POST /control_panel/device/create/` — criar dispositivo via admin (`CreateDevice`)
	- `PATCH /control_panel/device/<pk>/update/` — atualizar dispositivo específico (`UpdateDevice`)
	- `GET /control_panel/device/<pk>/detail/` — detalhes de um dispositivo (`DeviceDetail`)
	- `POST /control_panel/item/create/` — criar item do menu (`CreateMenuItem` in control_panel)
	- `PATCH /control_panel/item/<pk>/update/` — atualizar item do menu (`UpdateMenuItem`)
	- `DELETE /control_panel/item/<pk>/delete/` — deletar item do menu (`DeleteMenuItem`)
	- `GET /control_panel/orders/delivered/` — listar pedidos entregues (`DeliveredOrders`)
	- `GET /control_panel/orders/pending/` — listar pedidos pendentes (`PendingOrders`)
	- `GET /control_panel/order/<pk>/detail/` — detalhe de um pedido (`OrderDetail`)

- Menu público (`restaurant_menu` — prefixo `/menu/`):
	- `GET /menu/` — listar itens ativos do menu (`MenuItems`)
	- `GET /menu/item/<pk>/detail/` — detalhe de um item ativo (`MenuItemDetail`)
	- Observação: não há rota de criação de item em `restaurant_menu` — use `/control_panel/item/create/` (admin) para criar itens do menu

- Carrinho (`cart` — prefixo `/cart/`):
	- `POST /cart/cancel/` — cancelar o carrinho ativo (`CancelCart`)
	- `GET /cart/detail/` — ver o carrinho ativo (`CartDetail`)
	- `POST /cart/item/<pk>/add/` — adicionar/atualizar quantidade de item no carrinho (`AddMenuItemToCart`)
	- `DELETE /cart/item/<pk>/remove/` — remover/diminuir quantidade do item no carrinho (`RemoveMenuItemFromCart`)

- Pagamento (`payment` — prefixo `/payment/`):
	- `POST /payment/payment/` — criar ordem no Mercado Pago para o carrinho atual (`MPPayment`)
	- `POST /payment/webhook/` — endpoint público para receber notificações do Mercado Pago (`WebHook`)

- Cozinha (`kitchen` — prefixo `/kitchen/`):
	- `GET /kitchen/orders/` — listar pedidos não entregues (`Orders`)
	- `PATCH /kitchen/order/<pk>/deliver/` — marcar pedido como entregue (`DeliverOrder`)

## Autenticação

O projeto usa tokens (DRF TokenAuthentication). Envie `Authorization: Token <login_token>` nas requisições que exigem autenticação.

## Admin Django

- Admin disponível em `/admin/`.
- É possível criar um superusuário via endpoint `POST /device/register/admin/` (usa `CREATE_SUPERUSER_TOKEN`).

## Observações e próximos passos

- O projeto está organizado e pronto para rodar com Docker.
- Testes unitários são definidos nos arquivos `tests.py` de cada app (rodar `python manage.py test`).