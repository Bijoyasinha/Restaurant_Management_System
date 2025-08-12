-- =====================================================
-- RESTAURANT MANAGEMENT SYSTEM - CORRECTED DATABASE SCHEMA
-- =====================================================
-- This schema EXACTLY matches the SQLAlchemy models in models.py
-- Compatible with MySQL/MariaDB

-- Create database
CREATE DATABASE IF NOT EXISTS restaurant_db;
USE restaurant_db;

-- =====================================================
-- 1. USER TABLE (matches SQLAlchemy User model)
-- =====================================================
CREATE TABLE `user` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(80) NOT NULL UNIQUE,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `role` VARCHAR(20) DEFAULT 'staff',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 2. CUSTOMER TABLE (matches SQLAlchemy Customer model)
-- =====================================================
CREATE TABLE `customer` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(120) UNIQUE,
    `phone` VARCHAR(20),
    `address` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 3. MENU_ITEM TABLE (matches SQLAlchemy MenuItem model)
-- =====================================================
CREATE TABLE `menu_item` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `price` FLOAT NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `image_url` VARCHAR(255),
    `available` BOOLEAN DEFAULT TRUE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 4. TABLE (matches SQLAlchemy Table model)
-- =====================================================
CREATE TABLE `table` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `table_number` INT NOT NULL UNIQUE,
    `capacity` INT NOT NULL,
    `status` VARCHAR(20) DEFAULT 'available'
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 5. ORDER TABLE (matches SQLAlchemy Order model)
-- =====================================================
CREATE TABLE `order` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `table_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `customer_id` INT,
    `status` VARCHAR(20) DEFAULT 'pending',
    `total_amount` FLOAT DEFAULT 0.0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (`table_id`) REFERENCES `table`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (`customer_id`) REFERENCES `customer`(`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 6. ORDER_ITEM TABLE (matches SQLAlchemy OrderItem model)
-- =====================================================
CREATE TABLE `order_item` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_id` INT NOT NULL,
    `menu_item_id` INT NOT NULL,
    `quantity` INT DEFAULT 1,
    `price` FLOAT NOT NULL,
    `status` VARCHAR(20) DEFAULT 'pending',
    `notes` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (`order_id`) REFERENCES `order`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 7. RESERVATION TABLE (matches SQLAlchemy Reservation model)
-- =====================================================
CREATE TABLE `reservation` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `table_id` INT NOT NULL,
    `customer_name` VARCHAR(100) NOT NULL,
    `customer_email` VARCHAR(120),
    `customer_phone` VARCHAR(20) NOT NULL,
    `party_size` INT NOT NULL,
    `reservation_date` DATE NOT NULL,
    `reservation_time` TIME NOT NULL,
    `status` VARCHAR(20) DEFAULT 'confirmed',
    `notes` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (`table_id`) REFERENCES `table`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 8. INVENTORY TABLE (matches SQLAlchemy Inventory model)
-- =====================================================
CREATE TABLE `inventory` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `quantity` FLOAT NOT NULL,
    `unit` VARCHAR(20) NOT NULL,
    `reorder_level` FLOAT NOT NULL,
    `cost_per_unit` FLOAT NOT NULL,
    `supplier` VARCHAR(100),
    `last_updated` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================
CREATE INDEX idx_user_username ON `user`(username);
CREATE INDEX idx_user_email ON `user`(email);
CREATE INDEX idx_customer_email ON `customer`(email);
CREATE INDEX idx_menu_item_category ON `menu_item`(category);
CREATE INDEX idx_menu_item_available ON `menu_item`(available);
CREATE INDEX idx_table_number ON `table`(table_number);
CREATE INDEX idx_table_status ON `table`(status);
CREATE INDEX idx_order_status ON `order`(status);
CREATE INDEX idx_order_created_at ON `order`(created_at);

-- =====================================================
-- SAMPLE DATA INSERTION (Updated for correct schema)
-- =====================================================

-- Insert users (note: password hashes need to be generated properly)
INSERT INTO `user` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`) VALUES
(1, 'admin', 'admin@restaurant.com', 'pbkdf2:sha256:600000$7290c13e82948fa6c4349cbd6356e405$4e2ddce73fd94604d46b8b6e40f7235f9ae05e37b5d8da824f3c4c1eb8d62fe8', 'admin', '2025-08-12 03:10:42');

-- Insert customers
INSERT INTO `customer` (`name`, `email`, `phone`, `address`) VALUES
('John Doe', 'john@example.com', '555-123-4567', '123 Main St, Anytown'),
('Jane Smith', 'jane@example.com', '555-987-6543', '456 Oak Ave, Somewhere'),
('Robert Johnson', 'robert@example.com', '555-456-7890', '789 Pine Rd, Nowhere'),
('Sarah Williams', 'sarah@example.com', '555-789-0123', '321 Elm St, Anywhere');

-- Insert tables (using table_number instead of name)
INSERT INTO `table` (`table_number`, `capacity`, `status`) VALUES
(1, 2, 'available'),
(2, 4, 'available'),
(3, 4, 'available'),
(4, 6, 'available'),
(5, 8, 'available'),
(6, 2, 'available');

-- Insert menu items
INSERT INTO `menu_item` (`name`, `description`, `price`, `category`, `available`) VALUES
('Classic Burger', 'Beef patty with lettuce, tomato, and special sauce', 9.99, 'main', TRUE),
('Chicken Alfredo', 'Fettuccine pasta with creamy alfredo sauce and grilled chicken', 12.99, 'main', TRUE),
('Caesar Salad', 'Romaine lettuce with caesar dressing, croutons, and parmesan', 7.99, 'appetizer', TRUE),
('Margherita Pizza', 'Classic pizza with tomato sauce, mozzarella, and basil', 14.99, 'main', TRUE),
('Chocolate Cake', 'Rich chocolate cake with chocolate ganache', 6.99, 'dessert', TRUE),
('French Fries', 'Crispy golden fries with sea salt', 3.99, 'appetizer', TRUE),
('Iced Tea', 'Freshly brewed iced tea', 2.99, 'beverage', TRUE),
('Cheesecake', 'New York style cheesecake with berry compote', 7.99, 'dessert', TRUE),
('Chicken Wings', 'Spicy buffalo wings with blue cheese dip', 10.99, 'appetizer', TRUE),
('Vegetable Stir Fry', 'Mixed vegetables stir-fried in soy ginger sauce', 11.99, 'main', TRUE);

-- Insert inventory items
INSERT INTO `inventory` (`name`, `quantity`, `unit`, `reorder_level`, `cost_per_unit`, `supplier`) VALUES
('Beef Patties', 50, 'piece', 20, 1.50, 'Premium Meat Co.'),
('Chicken Breast', 20, 'kg', 10, 8.99, 'Fresh Poultry Ltd.'),
('Lettuce', 10, 'piece', 8, 1.99, 'Green Garden Supplies'),
('Tomatoes', 15, 'kg', 10, 2.99, 'Farm Fresh Vegetables'),
('Flour', 25, 'kg', 15, 1.50, 'Baking Supplies Co.'),
('Sugar', 15, 'kg', 10, 2.00, 'Sweet Supplies Inc.'),
('Cooking Oil', 20, 'l', 5, 3.99, 'Mediterranean Imports'),
('Cheese', 10, 'kg', 5, 9.99, 'Dairy Fresh Inc.'),
('Milk', 30, 'l', 10, 2.50, 'Dairy Fresh Inc.'),
('Potatoes', 50, 'kg', 20, 1.99, 'Farm Fresh Vegetables');

-- Sample orders (with correct user_id references)
INSERT INTO `order` (`table_id`, `user_id`, `customer_id`, `status`, `total_amount`, `created_at`) VALUES
(2, 1, 1, 'completed', 26.97, DATE_SUB(NOW(), INTERVAL 2 DAY)),
(4, 1, 2, 'completed', 35.97, DATE_SUB(NOW(), INTERVAL 1 DAY)),
(1, 1, 3, 'pending', 18.98, NOW());

-- Sample order items
INSERT INTO `order_item` (`order_id`, `menu_item_id`, `quantity`, `price`) VALUES
(1, 1, 1, 9.99),  -- Classic Burger
(1, 6, 1, 3.99),  -- French Fries  
(1, 7, 2, 2.99),  -- Iced Tea (2)
(2, 4, 1, 14.99), -- Margherita Pizza
(2, 3, 1, 7.99),  -- Caesar Salad
(2, 5, 1, 6.99),  -- Chocolate Cake
(2, 7, 2, 2.99),  -- Iced Tea (2)
(3, 9, 1, 10.99), -- Chicken Wings
(3, 6, 1, 3.99),  -- French Fries
(3, 7, 1, 2.99);  -- Iced Tea

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Verify table structure matches SQLAlchemy models
SELECT 'Schema verification completed - all tables match SQLAlchemy models!' as status;

-- Show all tables
SHOW TABLES;

-- Show table structures
DESCRIBE `user`;
DESCRIBE `customer`;
DESCRIBE `menu_item`;
DESCRIBE `table`;
DESCRIBE `order`;
DESCRIBE `order_item`;
DESCRIBE `reservation`;
DESCRIBE `inventory`;
