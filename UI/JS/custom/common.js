// Define your API URLs for various actions (CRUD operations)
var productListApiUrl = 'http://127.0.0.1:5000/getProducts';  // Fetch the list of products
var uomListApiUrl = 'http://127.0.0.1:5000/getUOM';  // Fetch the list of Unit of Measurements (UOM)
var productSaveApiUrl = 'http://127.0.0.1:5000/insertProduct';  // Save a new product
var productDeleteApiUrl = 'http://127.0.0.1:5000/deleteProduct';  // Delete a product
var orderListApiUrl = 'http://127.0.0.1:5000/getAllOrders';  // Fetch the list of all orders
var orderSaveApiUrl = 'http://127.0.0.1:5000/insertOrder';  // Save a new order

// External API for fetching product details (for product dropdown in order)
var productsApiUrl = 'https://fakestoreapi.com/products';

// Generic function to make API calls using jQuery's AJAX method
function callApi(method, url, data) {
    $.ajax({
        method: method,  // HTTP method (GET, POST, etc.)
        url: url,  // API URL
        data: data  // Data to send with the request
    }).done(function(msg) {
        window.location.reload();  // Reload the page after API call succeeds
    });
}

// Function to calculate the total price of all products in an order
function calculateValue() {
    var total = 0;  // Initialize total to 0
    $(".product-item").each(function(index) {  // Iterate over each product item
        var qty = parseFloat($(this).find('.product-qty').val());  // Get the quantity of the product
        var price = parseFloat($(this).find('#product_price').val());  // Get the price of the product
        price = price * qty;  // Calculate the total price for this product
        $(this).find('#item_total').val(price.toFixed(2));  // Set the total price for this product in the UI
        total += price;  // Add to the grand total
    });
    $("#product_grand_total").val(total.toFixed(2));  // Set the grand total in the UI
}

// Function to parse order data (custom format)
function orderParser(order) {
    return {
        id: order.id,  // Map order id
        date: order.employee_name,  // Use 'employee_name' as date (custom mapping)
        orderNo: order.employee_name,  // Use 'employee_name' as order number (custom mapping)
        customerName: order.employee_name,  // Use 'employee_name' as customer name (custom mapping)
        cost: parseInt(order.employee_salary)  // Convert employee salary to cost
    }
}

// Function to parse product data (custom format)
function productParser(product) {
    return {
        id: product.id,  // Map product id
        name: product.employee_name,  // Use 'employee_name' as product name (custom mapping)
        unit: product.employee_name,  // Use 'employee_name' as unit (custom mapping)
        price: product.employee_name  // Use 'employee_name' as price (custom mapping)
    }
}

// Function to parse product data for dropdown (custom format)
function productDropParser(product) {
    return {
        id: product.id,  // Map product id
        name: product.title  // Use product title as name
    }
}

// To enable bootstrap tooltip globally (commented out for now)
// $(function () {
//     $('[data-toggle="tooltip"]').tooltip()  // Initialize tooltips on elements with 'data-toggle="tooltip"'
// });
