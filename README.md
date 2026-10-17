#  E-Commerce API com Flask

API REST de um e-commerce simples, feita com **Python + Flask** e banco de dados **SQLite**. Permite cadastrar, listar, consultar, atualizar e remover produtos, com autenticação de usuários por sessão.

>  **Projeto de estudo.** Foi desenvolvido para praticar a criação de APIs, o uso de banco de dados com ORM e autenticação. Baseado no curso introdutório de Python e Flask da RocketSeat.

---

##  Funcionalidades

- Login e logout de usuários (autenticação por sessão com Flask-Login)
- CRUD completo de produtos:
  - **C**reate: cadastrar produto
  - **R**ead: listar todos e ver detalhes de um produto
  - **U**pdate: atualizar nome, preço e/ou descrição
  - **D**elete: remover produto
- Validação básica dos dados enviados e respostas em JSON com os códigos HTTP adequados (`200`, `400`, `401`, `404`)
- CORS habilitado, para ser consumida por um front-end em outro endereço

---

## Tecnologias

| Tecnologia | Para que serve |
|---|---|
| [Python](https://www.python.org/) | Linguagem do projeto |
| [Flask](https://flask.palletsprojects.com/) | Framework web que cria as rotas da API |
| [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) | ORM: permite usar classes Python no lugar de SQL |
| [SQLite](https://www.sqlite.org/) | Banco de dados em arquivo, sem precisar instalar nada |
| [Flask-Login](https://flask-login.readthedocs.io/) | Controle de login e rotas protegidas |
| [Flask-CORS](https://flask-cors.readthedocs.io/) | Libera acesso à API por outros domínios |

---

##  Como rodar o projeto

### Pré-requisitos

- Python 3.10 ou superior
- Git

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/artch43/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

**2. Crie e ative um ambiente virtual**

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

Quando o ambiente estiver ativo, aparece `(venv)` no início da linha do terminal.

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Crie o banco de dados** (veja a próxima seção) **e inicie o servidor**

```bash
python app.py
```

A API fica disponível em `http://127.0.0.1:5000`. Para testar se está funcionando, acesse `http://127.0.0.1:5000/teste`: a resposta deve ser `Hello, World`.

---

## Criando um usuário

O projeto ainda **não tem uma rota de cadastro de usuários**. Por isso, o primeiro usuário é criado pelo terminal, usando o `flask shell`:

```bash
flask shell
```

Dentro do shell, rode:

```python
db.create_all()                                   # cria as tabelas no banco
user = User(username="admin", password="123")     # cria o usuário
db.session.add(user)
db.session.commit()
exit()
```

Pronto: agora você já pode fazer login com `admin` / `123`.

> O arquivo do banco (`instance/ecommerce.db`) é criado na sua máquina e **não** vai para o GitHub (está no `.gitignore`). Cada pessoa gera o seu.

---

##  Rotas da API

Rotas marcadas com 🔒 exigem login (a sessão é mantida por cookie).

### Autenticação

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/login` | Faz login | ❌ |
| `POST` | `/logout` | Faz logout | 🔒 |

**Corpo do `POST /login`:**

```json
{
  "username": "admin",
  "password": "123"
}
```

Respostas: `200` login realizado, `401` credenciais inválidas.

### Produtos

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `GET` | `/api/products` | Lista todos os produtos (id, nome e preço) | ❌ |
| `GET` | `/api/products/<id>` | Detalhes de um produto (inclui descrição) | 🔒 |
| `POST` | `/api/products/add` | Cadastra um produto | 🔒 |
| `PUT` | `/api/products/update/<id>` | Atualiza um produto (campos opcionais) | ❌ |
| `DELETE` | `/api/products/delete/<id>` | Remove um produto | 🔒 |

**Corpo do `POST /api/products/add`:** `name` e `price` são obrigatórios; `description` é opcional.

```json
{
  "name": "Teclado Mecânico",
  "price": 249.90,
  "description": "Switch azul, layout ABNT2"
}
```

**Corpo do `PUT /api/products/update/<id>`:** envie apenas o que quiser alterar.

```json
{
  "price": 199.90
}
```

**Exemplo de resposta do `GET /api/products`:**

```json
[
  { "id": 1, "name": "Teclado Mecânico", "price": 249.9 }
]
```

### Códigos de resposta

| Código | Significado |
|---|---|
| `200` | Sucesso |
| `400` | Dados inválidos (ex.: faltou `name` ou `price`) |
| `401` | Não autorizado (sem login ou credenciais erradas) |
| `404` | Produto não encontrado |

---

## Modelagem do banco

**User**

| Campo | Tipo | Regras |
|---|---|---|
| `id` | Integer | Chave primária |
| `username` | String(80) | Obrigatório e único |
| `password` | String(80) | Opcional |

**Product**

| Campo | Tipo | Regras |
|---|---|---|
| `id` | Integer | Chave primária |
| `name` | String(120) | Obrigatório |
| `price` | Float | Obrigatório |
| `description` | Text | Opcional |

---

