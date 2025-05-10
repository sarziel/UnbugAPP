
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import StockItem, Supplier
from forms import StockItemForm, SearchForm
from datetime import datetime

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

@stock_bp.route('/')
@login_required
def index():
    search_form = SearchForm()
    query = StockItem.query
    
    if request.args.get('query'):
        search_term = f"%{request.args.get('query')}%"
        query = query.filter(StockItem.name.like(search_term) | 
                           StockItem.sku.like(search_term) |
                           StockItem.category.like(search_term))

    items = query.order_by(StockItem.name).all()
    low_stock_items = [item for item in items if item.is_low_stock()]

    return render_template('stock/index.html', 
                         items=items, 
                         low_stock_items=low_stock_items,
                         search_form=search_form)

@stock_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_item():
    form = StockItemForm()
    form.supplier_id.choices = [(0, 'Nenhum')] + [(s.id, s.name) for s in Supplier.query.filter_by(active=True).all()]
    
    if form.validate_on_submit():
        if StockItem.query.filter_by(sku=form.sku.data).first():
            flash('Já existe um item com este SKU.', 'danger')
            return render_template('stock/create.html', form=form)

        item = StockItem(
            name=form.name.data,
            description=form.description.data,
            sku=form.sku.data,
            category=form.category.data,
            quantity=form.quantity.data,
            minimum_stock=form.minimum_stock.data,
            unit_price=form.unit_price.data,
            location=form.location.data,
            supplier_id=form.supplier_id.data if form.supplier_id.data != 0 else None
        )
        
        db.session.add(item)
        db.session.commit()
        flash('Item adicionado com sucesso!', 'success')
        return redirect(url_for('stock.index'))
        
    return render_template('stock/create.html', form=form)
