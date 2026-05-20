# smart-restaurant-ordering

Protótipo de restaurante inteligente onde o pedido é feito por um tablet e, quando o pagamento é autorizado, o pedido é enviado para a cozinha. Neste momento, o projeto implementa apenas a autenticação e o gerenciamento de dispositivos internos (`checkout` e `kitchen`).

## Visão geral

- Protótipo backend em Django 6 com Django REST Framework.
- API para registro, login e gerenciamento de dispositivos.
- Autenticação de dispositivos via token UUID.
- Modelo de usuário customizado `Device` que representa dispositivos do restaurante.
- Dois tipos de dispositivo: `checkout` e `kitchen`.
- O fluxo de pedido e pagamento ainda não está implementado; atualmente apenas a autenticação de dispositivos existe.

## Principais funcionalidades

- Registrar dispositivos (`checkout` ou `kitchen`).
- Login de dispositivo com geração de token de autenticação DRF.
- Atualizar função do dispositivo autenticado.
- Atualizar senha do dispositivo autenticado.
- Criar superusuário via endpoint seguro.

## Estrutura do projeto

- `smart_restaurant/` - configurações do projeto Django.
- `devices/` - app principal com modelo, serializers, views, URLs, e validações.
- `Dockerfile` - imagem para rodar a API.
- `docker-compose.yml` - orquestra PostgreSQL e API.
- `.env` - variáveis de ambiente para banco e tokens.

## Tecnologias

- Python 3.12
- Django 6.0.5
- Django REST Framework 3.17.1
- PostgreSQL 16
- psycopg 3

## Endpoints

A API está disponível sob `/device/`.

- `POST /device/register/`
  - Registra novo dispositivo.
  - Campos: `username`, `password`, `confirm_password`, `device_authentication_token`, `function`.

- `POST /device/register/admin/`
  - Cria superusuário.
  - Campos: `username`, `password`, `confirm_password`, `create_admin_token`.

- `POST /device/login/`
  - Faz login de dispositivo.
  - Campos: `username`, `password`, `device_login_token`.
  - Retorna `login_token`.

- `PATCH /device/update/function/`
  - Atualiza a função do dispositivo autenticado.
  - Campos: `function`.

- `POST /device/update/password/`
  - Atualiza a senha do dispositivo autenticado.
  - Campos: `new_password`, `confirm_new_password`, `device_reset_password_token`.

## Variáveis de ambiente

O projeto exige as seguintes variáveis no arquivo `.env`:

- `POSTGRES_HOST`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `DEVICE_AUTHENTICATION_TOKEN`
- `DEVICE_LOGIN_TOKEN`
- `DEVICE_RESET_PASSWORD_TOKEN`
- `CREATE_SUPERUSER_TOKEN`

## Execução com Docker

1. Configure o arquivo `.env` com os valores desejados.
2. Execute:

```bash
docker compose up --build
```

A aplicação ficará disponível em `http://localhost:8000`.

## Observações

- A autenticação da API usa `TokenAuthentication` do Django REST Framework.
- O modelo de usuário padrão foi substituído por `devices.Device` com campo `function`.
- As senhas devem ter pelo menos 8 caracteres e não podem conter espaços.
- O projeto é um protótipo: ainda não há fluxo completo de pedidos pagos nem transmissão real para a cozinha, apenas autenticação de dispositivos.

## Admin Django

A interface administrativa está em `/admin/`. Para acessar, crie um superusuário via `POST /device/register/admin/`.
