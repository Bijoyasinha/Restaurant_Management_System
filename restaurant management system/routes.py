from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, MenuItem, Table, Order, OrderItem, Reservation, Inventory, Customer
from forms import LoginForm, RegistrationForm, MenuItemForm, TableForm, ReservationForm, OrderForm, OrderItemForm, InventoryForm, CustomerForm
from datetime import datetime

from extensions import db, login_manager

def register_routes(app):
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Authentication routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Login unsuccessful. Please check username and password', 'danger')
        
        return render_template('auth/login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in', 'success')
            return redirect(url_for('login'))
        
        return render_template('auth/register.html', form=form)
    
    # Dashboard route
    @app.route('/dashboard')
    @login_required
    def dashboard():
        from datetime import date, timedelta
        from sqlalchemy import func
        
        # Get basic counts
        total_orders = Order.query.count()
        active_orders = Order.query.filter(Order.status.in_(['pending', 'preparing'])).count()
        total_customers = Customer.query.count()
        total_tables = Table.query.count()
        available_tables = Table.query.filter_by(status='available').count()
        occupied_tables = Table.query.filter_by(status='occupied').count()
        
        # Calculate today's revenue
        today = date.today()
        today_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            func.date(Order.created_at) == today,
            Order.status == 'completed'
        ).scalar() or 0
        
        # Calculate yesterday's revenue for comparison
        yesterday = today - timedelta(days=1)
        yesterday_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            func.date(Order.created_at) == yesterday,
            Order.status == 'completed'
        ).scalar() or 0
        
        # Calculate revenue change percentage
        if yesterday_revenue > 0:
            revenue_change = round(((today_revenue - yesterday_revenue) / yesterday_revenue) * 100, 1)
        else:
            revenue_change = 0
        
        # Get new customers this week
        week_ago = today - timedelta(days=7)
        new_customers = Customer.query.filter(func.date(Customer.created_at) >= week_ago).count()
        
        # Create stats object
        stats = {
            'total_orders': total_orders,
            'active_orders': active_orders,
            'today_revenue': f"{today_revenue:.2f}",
            'revenue_change': revenue_change,
            'total_customers': total_customers,
            'new_customers': new_customers,
            'total_tables': total_tables,
            'available_tables': available_tables,
            'occupied_tables': occupied_tables
        }
        
        # Get recent orders (last 10)
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        
        # Get popular menu items (based on order frequency)
        popular_items_query = db.session.query(
            MenuItem.id,
            MenuItem.name,
            MenuItem.category,
            MenuItem.price,
            func.count(OrderItem.id).label('order_count')
        ).join(OrderItem).group_by(MenuItem.id).order_by(func.count(OrderItem.id).desc()).limit(5).all()
        
        popular_items = []
        for item in popular_items_query:
            popular_items.append({
                'name': item.name,
                'category': item.category,
                'price': item.price,
                'order_count': item.order_count
            })
        
        return render_template('dashboard.html', 
                              stats=stats,
                              recent_orders=recent_orders,
                              popular_items=popular_items)
    
    # Customer routes
    @app.route('/customers')
    @login_required
    def customer_list():
        customers = Customer.query.all()
        return render_template('customers/list.html', customers=customers)
    
    @app.route('/customers/add', methods=['GET', 'POST'])
    @login_required
    def customer_add():
        form = CustomerForm()
        if form.validate_on_submit():
            customer = Customer(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                address=form.address.data
            )
            db.session.add(customer)
            db.session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('customer_list'))
        
        return render_template('customers/form.html', form=form)
    
    @app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def customer_edit(id):
        customer = Customer.query.get_or_404(id)
        form = CustomerForm(obj=customer)
        
        if form.validate_on_submit():
            customer.name = form.name.data
            customer.email = form.email.data
            customer.phone = form.phone.data
            customer.address = form.address.data
            
            db.session.commit()
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('customer_list'))
        
        return render_template('customers/form.html', form=form, customer=customer)
    
    @app.route('/customers/delete/<int:id>', methods=['POST'])
    @login_required
    def customer_delete(id):
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully!', 'success')
        return redirect(url_for('customer_list'))
    
    # Menu routes
    @app.route('/menu')
    @login_required
    def menu_list():
        menu_items = MenuItem.query.all()
        return render_template('menu/list.html', menu_items=menu_items)
    
    @app.route('/menu/add', methods=['GET', 'POST'])
    @login_required
    def menu_add():
        form = MenuItemForm()
        if form.validate_on_submit():
            menu_item = MenuItem(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                category=form.category.data,
                image_url=form.image_url.data,
                available=form.available.data
            )
            db.session.add(menu_item)
            db.session.commit()
            flash('Menu item added successfully!', 'success')
            return redirect(url_for('menu_list'))
        
        return render_template('menu/form.html', form=form)
    
    @app.route('/menu/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def menu_edit(id):
        menu_item = MenuItem.query.get_or_404(id)
        form = MenuItemForm(obj=menu_item)
        
        if form.validate_on_submit():
            menu_item.name = form.name.data
            menu_item.description = form.description.data
            menu_item.price = form.price.data
            menu_item.category = form.category.data
            menu_item.image_url = form.image_url.data
            menu_item.available = form.available.data
            
            db.session.commit()
            flash('Menu item updated successfully!', 'success')
            return redirect(url_for('menu_list'))
        
        return render_template('menu/form.html', form=form, menu_item=menu_item)
    
    @app.route('/menu/delete/<int:id>', methods=['POST'])
    @login_required
    def menu_delete(id):
        menu_item = MenuItem.query.get_or_404(id)
        db.session.delete(menu_item)
        db.session.commit()
        flash('Menu item deleted successfully!', 'success')
        return redirect(url_for('menu_list'))
    
    # Table routes
    @app.route('/tables')
    @login_required
    def table_list():
        tables = Table.query.all()
        return render_template('tables/list.html', tables=tables)
    
    @app.route('/tables/add', methods=['GET', 'POST'])
    @login_required
    def table_add():
        form = TableForm()
        if form.validate_on_submit():
            table = Table(
                table_number=form.table_number.data,
                capacity=form.capacity.data,
                status=form.status.data
            )
            db.session.add(table)
            db.session.commit()
            flash('Table added successfully!', 'success')
            return redirect(url_for('table_list'))
        
        return render_template('tables/form.html', form=form)
    
    @app.route('/tables/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def table_edit(id):
        table = Table.query.get_or_404(id)
        form = TableForm(obj=table)
        
        if form.validate_on_submit():
            table.table_number = form.table_number.data
            table.capacity = form.capacity.data
            table.status = form.status.data
            
            db.session.commit()
            flash('Table updated successfully!', 'success')
            return redirect(url_for('table_list'))
        
        return render_template('tables/form.html', form=form, table=table)
    
    # Order routes
    @app.route('/orders')
    @login_required
    def order_list():
        orders = Order.query.all()
        return render_template('orders/list.html', orders=orders)
    
    @app.route('/orders/add', methods=['GET', 'POST'])
    @login_required
    def order_add():
        form = OrderForm()
        form.table_id.choices = [(t.id, f'Table {t.table_number}') for t in Table.query.filter_by(status='available').all()]
        form.customer_id.choices = [(c.id, c.name) for c in Customer.query.all()]
        
        if form.validate_on_submit():
            order = Order(
                table_id=form.table_id.data,
                user_id=current_user.id,
                customer_id=form.customer_id.data,
                status='pending'
            )
            db.session.add(order)
            
            # Update table status
            table = Table.query.get(form.table_id.data)
            table.status = 'occupied'
            
            db.session.commit()
            
            flash('Order created! Now add items to the order.', 'success')
            return redirect(url_for('order_items', order_id=order.id))
        
        return render_template('orders/form.html', form=form)
    
    @app.route('/orders/<int:order_id>/items', methods=['GET', 'POST'])
    @login_required
    def order_items(order_id):
        order = Order.query.get_or_404(order_id)
        menu_items = MenuItem.query.filter_by(available=True).all()
        form = OrderItemForm()
        form.menu_item_id.choices = [(m.id, f'{m.name} (${m.price:.2f})') for m in menu_items]
        
        if form.validate_on_submit():
            menu_item = MenuItem.query.get(form.menu_item_id.data)
            if menu_item:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    quantity=form.quantity.data,
                    price=menu_item.price,
                    notes=form.notes.data
                )
                db.session.add(order_item)
                
                # Update order total
                order.total_amount += (menu_item.price * form.quantity.data)
                
                db.session.commit()
                flash('Item added to order!', 'success')
            
            return redirect(url_for('order_items', order_id=order.id))
        
        return render_template('orders/items.html', order=order, form=form, menu_items=menu_items)
    
    @app.route('/orders/<int:order_id>/items/<int:item_id>/delete', methods=['POST'])
    @login_required
    def order_item_delete(order_id, item_id):
        order_item = OrderItem.query.get_or_404(item_id)
        order = Order.query.get_or_404(order_id)
        
        # Update order total
        order.total_amount -= (order_item.price * order_item.quantity)
        
        db.session.delete(order_item)
        db.session.commit()
        
        flash('Item removed from order!', 'success')
        return redirect(url_for('order_items', order_id=order_id))
    
    @app.route('/orders/<int:order_id>/complete', methods=['POST'])
    @login_required
    def order_complete(order_id):
        order = Order.query.get_or_404(order_id)
        order.status = 'completed'
        
        # Update table status
        table = Table.query.get(order.table_id)
        table.status = 'available'
        
        db.session.commit()
        flash('Order completed!', 'success')
        return redirect(url_for('order_list'))
    
    @app.route('/orders/<int:order_id>/cancel', methods=['POST'])
    @login_required
    def order_cancel(order_id):
        order = Order.query.get_or_404(order_id)
        order.status = 'cancelled'
        
        # Update table status
        table = Table.query.get(order.table_id)
        table.status = 'available'
        
        db.session.commit()
        flash('Order cancelled!', 'success')
        return redirect(url_for('order_list'))
    
    # API routes for POS system
    @app.route('/api/menu')
    def api_menu():
        menu_items = MenuItem.query.filter_by(available=True).all()
        menu_data = [{
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'category': item.category,
            'image_url': item.image_url
        } for item in menu_items]
        
        return jsonify(menu_data)
    
    @app.route('/api/tables')
    def api_tables():
        tables = Table.query.all()
        table_data = [{
            'id': table.id,
            'table_number': table.table_number,
            'capacity': table.capacity,
            'status': table.status
        } for table in tables]
        
        return jsonify(table_data)
    
    @app.route('/api/customers')
    def api_customers():
        customers = Customer.query.all()
        customer_data = [{
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone
        } for customer in customers]
        
        return jsonify(customer_data)
    
    @app.route('/api/orders', methods=['POST'])
    def api_create_order():
        data = request.json
        
        if not data or 'table_id' not in data or 'items' not in data:
            return jsonify({'error': 'Invalid data'}), 400
        
        # Create new order
        order = Order(
            table_id=data['table_id'],
            user_id=data.get('user_id', 1),  # Default to first user if not provided
            customer_id=data.get('customer_id'),
            status='pending'
        )
        db.session.add(order)
        db.session.commit()
        
        # Add order items
        total_amount = 0
        for item_data in data['items']:
            menu_item = MenuItem.query.get(item_data['menu_item_id'])
            if not menu_item:
                continue
                
            quantity = item_data.get('quantity', 1)
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=quantity,
                price=menu_item.price,
                notes=item_data.get('notes', '')
            )
            db.session.add(order_item)
            total_amount += (menu_item.price * quantity)
        
        # Update order total and table status
        order.total_amount = total_amount
        table = Table.query.get(data['table_id'])
        table.status = 'occupied'
        
        db.session.commit()
        
        return jsonify({
            'order_id': order.id,
            'total_amount': order.total_amount,
            'status': order.status
        }), 201