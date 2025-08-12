

# Restaurant Management System

Group Member 1 
Name: Bijoya Sinha
Id: 231-115-033
Group Member 2
Name: Papia Jahan Jabin
Id: 231-115-021

## Contribution of Group Members:

Bijoya Sinha (ID: 231-115-033) was responsible for designing and implementing 
the Menu Management and Table Management modules, including developing Flask 
routes for adding, editing, and updating menu items and table statuses. 
She also worked on the frontend templates for the menu and table pages, 
ensuring a user-friendly interface, and contributed to the database design by 
helping create the restaurant_db.sql file.

Papia Jahan Jabin (ID: 231-115-021) focused on implementing the Order Management 
and Customer Management features, enabling the creation, tracking, and management 
of orders and customer records. She also developed the User Authentication system 
to ensure secure staff logins, created the Dashboard view to display key restaurant 
operational metrics, and worked on the init_db.py script to integrate MySQL with
Flask seamlessly.


<img width="3840" height="2739" alt="ERD " src="https://github.com/user-attachments/assets/17e4302b-1c7c-4f7f-8b26-099b196239a2" />


A comprehensive restaurant management system built with Python Flask and MySQL, designed to help restaurant owners manage their menu, orders, tables, and customers efficiently.

## Features

- **Menu Management**: Add, edit, and delete menu items with categories, prices, and availability status
- **Order Management**: Create and manage orders, add items to orders, and track order status
- **Table Management**: Manage restaurant tables, track table status (available, occupied, reserved)
- **Customer Management**: Maintain a database of customers for orders and reservations
- **User Authentication**: Secure login system for staff members
- **Dashboard**: Overview of restaurant operations with key metrics

## Prerequisites

- Python 3.7 or higher
- MySQL (XAMPP recommended)
- pip (Python package manager)

## Installation

1. Clone or download this repository to your local machine

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:
   - Start XAMPP and ensure MySQL service is running
   - Import the `restaurant_db.sql` file into your MySQL server using phpMyAdmin or MySQL command line

4. Configure environment variables:
   - Rename `.env.example` to `.env` (if not already done)
   - Update the database credentials in the `.env` file to match your MySQL setup

5. Initialize the database:
   ```
   python init_db.py
   ```

## Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Login with the default admin credentials:
   - Email: admin@restaurant.com
   - Password: admin123

## Project Structure

- `app.py`: Main application file
- `models.py`: Database models
- `forms.py`: Form definitions using Flask-WTF
- `routes.py`: Application routes and views
- `init_db.py`: Database initialization script
- `templates/`: HTML templates
- `restaurant_db.sql`: SQL file for database setup

## Usage

### Menu Management
- Navigate to the Menu section to add, edit, or delete menu items
- Organize items by category and set availability status

### Order Management
- Create new orders by selecting a customer and table
- Add menu items to orders with quantities
- Complete or cancel orders as needed

### Table Management
- Add tables with capacity information
- View table status (available, occupied, reserved)
- Create orders directly from the table view

### Customer Management
- Maintain a database of customers with contact information
- Associate customers with orders for better tracking

## Security Notes

- Change the default admin password after first login
- Update the SECRET_KEY in the .env file for production use
- Implement additional security measures for production deployment

## License

This project is licensed under the MIT License - see the LICENSE file for details.
