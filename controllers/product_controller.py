from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from services.products_service import ProductService
from models.products import Products, db

product_blueprint = Blueprint('products', __name__)

@product_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.form
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
   
    ProductService.create_product(name, description)
    return redirect(url_for('products.index'))


@product_blueprint.route('/update/<id>',methods=['POST','GET'])
def update_product(id):
    prod = Products.query.get(id)
    if request.method == 'POST':
        data=request.form
        prod.name=data.get('name')
        prod.description=data.get('description')
        
        db.session.commit()
        return redirect(url_for('products.index'))
    
    return render_template('update.html',prod=prod)

@product_blueprint.route('/delete/<id>')
def delete_product(id):
    prod = Products.query.get(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for('products.index'))

@product_blueprint.route('/')
def index():
    prods = Products.query.all()

    return render_template('index.html',prods=prods)