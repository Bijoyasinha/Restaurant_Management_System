// Restaurant Management System - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
    
    // Order page - Update total amount when quantity changes
    const quantityInputs = document.querySelectorAll('.item-quantity');
    if (quantityInputs.length > 0) {
        quantityInputs.forEach(input => {
            input.addEventListener('change', updateOrderTotal);
        });
    }
    
    // Function to update order total
    function updateOrderTotal() {
        const items = document.querySelectorAll('.order-item');
        let total = 0;
        
        items.forEach(item => {
            const price = parseFloat(item.querySelector('.item-price').dataset.price);
            const quantity = parseInt(item.querySelector('.item-quantity').value);
            const subtotal = price * quantity;
            
            item.querySelector('.item-subtotal').textContent = '$' + subtotal.toFixed(2);
            total += subtotal;
        });
        
        document.querySelector('.order-total').textContent = '$' + total.toFixed(2);
    }
    
    // Dashboard charts initialization (if Chart.js is included)
    if (typeof Chart !== 'undefined' && document.getElementById('salesChart')) {
        const ctx = document.getElementById('salesChart').getContext('2d');
        const salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                datasets: [{
                    label: 'Sales ($)',
                    data: [1200, 1900, 1500, 2000, 2500, 3000, 2800],
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Table filter functionality
    const tableFilter = document.getElementById('tableFilter');
    if (tableFilter) {
        tableFilter.addEventListener('change', function() {
            const status = this.value;
            const tables = document.querySelectorAll('.table-card');
            
            tables.forEach(table => {
                if (status === 'all' || table.dataset.status === status) {
                    table.style.display = 'block';
                } else {
                    table.style.display = 'none';
                }
            });
        });
    }
    
    // Menu category filter
    const menuFilter = document.getElementById('menuFilter');
    if (menuFilter) {
        menuFilter.addEventListener('change', function() {
            const category = this.value;
            const menuItems = document.querySelectorAll('.menu-item-card');
            
            menuItems.forEach(item => {
                if (category === 'all' || item.dataset.category === category) {
                    item.closest('.col-md-4').style.display = 'block';
                } else {
                    item.closest('.col-md-4').style.display = 'none';
                }
            });
        });
    }
    
    // Confirm delete modals
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
});