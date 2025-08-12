from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, IntegerField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from models import User, Table, Customer
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')

class CustomerForm(FlaskForm):
    name = StringField('Customer Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    address = TextAreaField('Address')
    submit = SubmitField('Save Customer')
    
    def validate_email(self, email):
        if email.data:
            customer = Customer.query.filter_by(email=email.data).first()
            if customer and customer.id != getattr(self, 'id', None):
                raise ValidationError('Email is already registered. Please use a different one.')

class MenuItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', choices=[
        ('appetizer', 'Appetizer'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage')
    ], validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    available = BooleanField('Available', default=True)
    submit = SubmitField('Save Menu Item')

class TableForm(FlaskForm):
    table_number = IntegerField('Table Number', validators=[DataRequired(), NumberRange(min=1)])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])
    status = SelectField('Status', choices=[
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Table')
    
    def validate_table_number(self, table_number):
        table = Table.query.filter_by(table_number=table_number.data).first()
        if table and table.id != getattr(self, 'id', None):
            raise ValidationError('Table number already exists. Please choose a different one.')

class ReservationForm(FlaskForm):
    table_id = SelectField('Table', coerce=int, validators=[DataRequired()])
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=100)])
    customer_email = StringField('Email', validators=[Email()])
    customer_phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    party_size = IntegerField('Party Size', validators=[DataRequired(), NumberRange(min=1)])
    reservation_date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    reservation_time = TimeField('Time', validators=[DataRequired()], format='%H:%M')
    notes = TextAreaField('Notes')
    status = SelectField('Status', choices=[
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='confirmed')
    submit = SubmitField('Save Reservation')
    
    def validate_party_size(self, party_size):
        if hasattr(self, 'table_id') and self.table_id.data:
            table = Table.query.get(self.table_id.data)
            if table and party_size.data > table.capacity:
                raise ValidationError(f'Party size exceeds table capacity ({table.capacity}).')

class OrderForm(FlaskForm):
    table_id = SelectField('Table', coerce=int, validators=[DataRequired()])
    customer_id = SelectField('Customer', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Order')

class OrderItemForm(FlaskForm):
    menu_item_id = SelectField('Menu Item', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1)
    notes = TextAreaField('Special Instructions')
    submit = SubmitField('Add to Order')

class InventoryForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    unit = SelectField('Unit', choices=[
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('piece', 'Piece')
    ], validators=[DataRequired()])
    reorder_level = FloatField('Reorder Level', validators=[DataRequired(), NumberRange(min=0)])
    cost_per_unit = FloatField('Cost per Unit', validators=[DataRequired(), NumberRange(min=0)])
    supplier = StringField('Supplier', validators=[Length(max=100)])
    submit = SubmitField('Save Inventory Item')