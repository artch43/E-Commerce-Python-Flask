from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

# Modelagem 
# User (id, username, password)
class User(db.Model, UserMixin): #essa clase UserMixin já tem alguns parametros definidos (heranca)
    id = db.Column(db.Integer, primary_key=True) #cria uma coluna com o ID, que deve ser unico
    username = db.Column(db.String(80), nullable=False, unique=True) #username vai receber uma string de no max 80caract, nao pode ser nulo e será unico
    password = db.Column(db.String(80), nullable=True) #senha vai receber string de no max 80caract, senha nao precisa ser unique

# Produto (id, name, price, description)
class Product(db.Model): 
    id = db.Column(db.Integer, primary_key=True) #ID deve ser unico
    name = db.Column(db.String(120), nullable=False) #nao quero q ela possa ser nulo; string tem limite
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True) #Text nao tem limite de texto e pode ser nulo


#Autenticacao
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data.get("username")).first() #se nao tiver esse usuario, retorna none

    if user and data.get("password") == user.password: #verificando se exite no banco de dados, e se a senha q ele enviou é a mesma salva no DB
            login_user(user)
            return jsonify({"message": "Logged in successfully"})
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully"})



#Definindo rota para adicionar produtos na API com o metodo 'POST'
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data: #verifica se data e preco estao dentro de data, retornando o cadastro do produto
        product = Product(name=data["name"] ,price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400
    #ele DEVE ter essas duas condicoes pra cadastrar

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    # Recuperar produto da base de dados
    # Verificar se o produto existe
    # Se existe, apagar da db
    # Se nao existe, retornar 404
    product = Product.query.get(product_id)
    if product != None:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Product not found"}), 404


@app.route('/api/products/<int:product_id>', methods=["GET"]) #queremos recuperar os dados dos itens
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product != None:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }) #Lembrar que utilizamos o model que ta definido no banco de dados
    return jsonify({"message": "Product not found"}),404


@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_products(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}),404


    # é interessante ter um if para cada um, visto que ele pode atualizar apenas um elemento
    data = request.json
    if 'name' in data:
        product.name = data['name'] #altera o nome do produto pro novo nome

    if 'price' in data: 
        product.price = data['price'] 

    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({"message": "Product update successfully"})


@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
        product_list.append(product_data)

    return jsonify(product_list)

# Definir uma rota raiz (página inicial e a função que será executada ao requisitor)
@app.route('/teste') #
def hello_world():
    return 'Hello, World'


if __name__ == "__main__":
    app.run(debug=True) #Modo utilizado para desenvolvimento (não utilizado pra producao)
