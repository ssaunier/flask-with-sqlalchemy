try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass # Heroku does not use .env

from flask import Flask, render_template
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import product_schema, products_schema

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)

@app.route('/hello')
def hello():
    return "Hello world!"

@app.route('/products')
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

@app.route('/products/<int:id>')
def product(id):
    product = db.session.query(Product).get(id)
    return product_schema.jsonify(product)
