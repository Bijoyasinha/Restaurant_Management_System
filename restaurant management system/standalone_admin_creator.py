#!/usr/bin/env python3
"""
Standalone Admin User Creator for Restaurant Management System
This script directly connects to MySQL database and creates admin users
No dependency on Flask app - works independently
"""

import mysql.connector
import hashlib
import os
import secrets
from datetime import datetime

class AdminUserCreator:
    def __init__(self):
        """Initialize database connection"""
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',  # Default XAMPP MySQL password (empty)
            'database': 'restaurant_db'
        }
        self.conn = None
        
    def connect_database(self):
        """Connect to MySQL database"""
        try:
            print("🔗 Connecting to MySQL database...")
            self.conn = mysql.connector.connect(**self.db_config)
            print("✅ Database connection successful!")
            return True
        except mysql.connector.Error as err:
            print(f"❌ Database connection failed: {err}")
            print("\n🔧 Troubleshooting:")
            print("1. Make sure XAMPP MySQL is running")
            print("2. Check if 'restaurant_db' database exists")
            print("3. Verify MySQL credentials")
            return False
    
    def generate_password_hash(self, password):
        """Generate werkzeug-compatible password hash"""
        # This mimics Flask's generate_password_hash function
        salt = secrets.token_hex(16)
        iterations = 600000
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), iterations)
        hash_hex = hash_obj.hex()
        return f"pbkdf2:sha256:{iterations}${salt}${hash_hex}"
    
    def check_user_exists(self, username):
        """Check if user already exists"""
        cursor = self.conn.cursor()
        query = "SELECT id, username, role FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def create_admin_user(self, username, email, password, role='admin'):
        """Create new admin user in database"""
        try:
            cursor = self.conn.cursor()
            
            # Generate password hash
            password_hash = self.generate_password_hash(password)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert new user
            query = """
            INSERT INTO user (username, email, password_hash, role, created_at) 
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (username, email, password_hash, role, current_time)
            
            cursor.execute(query, values)
            self.conn.commit()
            
            user_id = cursor.lastrowid
            cursor.close()
            
            print(f"✅ Successfully created user!")
            print(f"   👤 Username: {username}")
            print(f"   📧 Email: {email}")
            print(f"   🔑 Password: {password}")
            print(f"   👑 Role: {role}")
            print(f"   🆔 User ID: {user_id}")
            
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Error creating user: {err}")
            return False
    
    def update_user_password(self, user_id, username, new_password, role='admin'):
        """Update existing user's password and role"""
        try:
            cursor = self.conn.cursor()
            
            # Generate new password hash
            password_hash = self.generate_password_hash(new_password)
            
            # Update user
            query = "UPDATE user SET password_hash = %s, role = %s WHERE id = %s"
            values = (password_hash, role, user_id)
            
            cursor.execute(query, values)
            self.conn.commit()
            cursor.close()
            
            print(f"✅ Successfully updated user '{username}'!")
            print(f"   🔑 New Password: {new_password}")
            print(f"   👑 Role: {role}")
            
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Error updating user: {err}")
            return False
    
    def list_all_users(self):
        """List all users in database"""
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, username, email, role, created_at FROM user ORDER BY created_at DESC"
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            
            if not users:
                print("📝 No users found in database.")
                return []
            
            print("\n👥 All Users in Database:")
            print("-" * 80)
            print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Role':<10} {'Created':<20}")
            print("-" * 80)
            
            for user in users:
                user_id, username, email, role, created_at = user
                created_str = created_at.strftime('%Y-%m-%d %H:%M:%S') if created_at else 'N/A'
                print(f"{user_id:<5} {username:<15} {email:<25} {role:<10} {created_str:<20}")
            
            print("-" * 80)
            return users
            
        except mysql.connector.Error as err:
            print(f"❌ Error listing users: {err}")
            return []
    
    def delete_user(self, user_id):
        """Delete user by ID"""
        try:
            cursor = self.conn.cursor()
            
            # First get user info
            query = "SELECT username FROM user WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            
            if not result:
                print(f"❌ User with ID {user_id} not found!")
                cursor.close()
                return False
            
            username = result[0]
            
            # Delete user
            query = "DELETE FROM user WHERE id = %s"
            cursor.execute(query, (user_id,))
            self.conn.commit()
            cursor.close()
            
            print(f"✅ Successfully deleted user '{username}' (ID: {user_id})")
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Error deleting user: {err}")
            return False
    
    def close_connection(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("🔒 Database connection closed.")

def main():
    """Main function"""
    print("🍽️  Restaurant Management System - Standalone Admin Creator")
    print("=" * 65)
    
    creator = AdminUserCreator()
    
    # Connect to database
    if not creator.connect_database():
        return
    
    try:
        while True:
            print("\n📋 Available Options:")
            print("1. Create new admin user")
            print("2. Create new staff user")
            print("3. Update existing user password")
            print("4. List all users")
            print("5. Delete user")
            print("6. Exit")
            
            choice = input("\n👉 Select option (1-6): ").strip()
            
            if choice == '1':
                print("\n👑 Creating Admin User")
                print("-" * 25)
                username = input("Enter username: ").strip()
                email = input("Enter email: ").strip()
                password = input("Enter password: ").strip()
                
                if not username or not email or not password:
                    print("❌ All fields are required!")
                    continue
                
                # Check if user exists
                existing = creator.check_user_exists(username)
                if existing:
                    print(f"⚠️  User '{username}' already exists!")
                    update = input("Update this user? (y/n): ").lower().strip()
                    if update == 'y':
                        creator.update_user_password(existing[0], username, password, 'admin')
                    continue
                
                creator.create_admin_user(username, email, password, 'admin')
                
            elif choice == '2':
                print("\n👨‍💼 Creating Staff User")
                print("-" * 25)
                username = input("Enter username: ").strip()
                email = input("Enter email: ").strip()
                password = input("Enter password: ").strip()
                
                if not username or not email or not password:
                    print("❌ All fields are required!")
                    continue
                
                # Check if user exists
                existing = creator.check_user_exists(username)
                if existing:
                    print(f"⚠️  User '{username}' already exists!")
                    continue
                
                creator.create_admin_user(username, email, password, 'staff')
                
            elif choice == '3':
                print("\n🔄 Update User Password")
                print("-" * 25)
                creator.list_all_users()
                user_id = input("\nEnter User ID to update: ").strip()
                
                try:
                    user_id = int(user_id)
                    new_password = input("Enter new password: ").strip()
                    new_role = input("Enter role (admin/staff/manager/chef): ").strip() or 'staff'
                    
                    if not new_password:
                        print("❌ Password is required!")
                        continue
                    
                    existing = creator.check_user_exists("")  # We'll check by ID in update function
                    creator.update_user_password(user_id, f"User_{user_id}", new_password, new_role)
                    
                except ValueError:
                    print("❌ Invalid User ID!")
                
            elif choice == '4':
                print("\n📋 Listing All Users")
                print("-" * 25)
                creator.list_all_users()
                
            elif choice == '5':
                print("\n🗑️  Delete User")
                print("-" * 15)
                creator.list_all_users()
                user_id = input("\nEnter User ID to delete: ").strip()
                
                try:
                    user_id = int(user_id)
                    confirm = input(f"Are you sure you want to delete user ID {user_id}? (y/n): ").lower().strip()
                    if confirm == 'y':
                        creator.delete_user(user_id)
                except ValueError:
                    print("❌ Invalid User ID!")
                
            elif choice == '6':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option! Please select 1-6.")
                
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        creator.close_connection()

if __name__ == "__main__":
    main()
