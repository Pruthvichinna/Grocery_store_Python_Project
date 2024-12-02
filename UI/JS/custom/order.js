// Initialize an empty object to store product prices by product ID
var productPrices = {};

$(function () {
    // Fetch product list via API when the page loads
    $.get(productListApiUrl, function (response) {
        productPrices = {};  // Reset productPrices object

        if(response) {
            var options = '<option value="">--Select--</option>';  // Default option in the dropdown

            // Loop through each product in the response and populate the dropdown
            $.each(response, function(index, product) {
                options += '<option value="'+ product.product_id +'">'+ product.name +'</option>';
                // Store product price using the product ID as the key
                productPrices[product.product_id] = product.price_per_unit;
            });

            // Update the product dropdown with the product options
            $(".product-box").find("select").empty().html(options);
        }
    });
});

// Event handler for the "Add More" button to add additional product rows
$("#addMoreButton").click(function () {
    var row = $(".product-box").html();  // Clone the HTML of the first product row
    $(".product-box-extra").append(row);  // Append the cloned row
    $(".product-box-extra .remove-row").last().removeClass('hideit');  // Make the "Remove" button visible for the new row
    $(".product-box-extra .product-price").last().text('0.0');  // Set default price to 0
    $(".product-box-extra .product-qty").last().val('1');  // Set default quantity to 1
    $(".product-box-extra .product-total").last().text('0.0');  // Set default total to 0
});

// Event handler for removing a product row from the cart
$(document).on("click", ".remove-row", function () {
    $(this).closest('.row').remove();  // Remove the closest product row
    calculateValue();  // Recalculate the total value after removal
});

// Event handler for changing the selected product in the dropdown
$(document).on("change", ".cart-product", function () {
    var product_id = $(this).val();  // Get the selected product ID
    var price = productPrices[product_id];  // Get the price for the selected product

    // Set the product price for the selected product in the row
    $(this).closest('.row').find('#product_price').val(price);
    calculateValue();  // Recalculate the total value after price change
});

// Event handler for changing the product quantity
$(document).on("change", ".product-qty", function () {
    calculateValue();  // Recalculate the total value when the quantity is changed
});

// Event handler for saving the order when the "Save Order" button is clicked
$("#saveOrder").on("click", function(){
    var formData = $("form").serializeArray();  // Serialize the form data into an array
    var requestPayload = {
        customer_name: null,
        total: null,
        order_details: []  // Array to hold order details
    };
    var orderDetails = [];

    // Loop through the form data to fill the request payload
    for(var i=0; i<formData.length; ++i) {
        var element = formData[i];
        var lastElement = null;  // To keep track of the last order detail object

        // Assign values to the requestPayload based on the form field names
        switch(element.name) {
            case 'customerName':
                requestPayload.customer_name = element.value;  // Set customer name
                break;
            case 'product_grand_total':
                requestPayload.grand_total = element.value;  // Set total price for the order
                break;
            case 'product':
                // Add a new product object to the order details
                requestPayload.order_details.push({
                    product_id: element.value,
                    quantity: null,
                    total_price: null
                });
                break;
            case 'qty':
                // Set the quantity for the last added product
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.quantity = element.value;
                break;
            case 'item_total':
                // Set the total price for the last added product
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.total_price = element.value;
                break;
        }
    }

    // Call the API to save the order with the request payload
    callApi("POST", orderSaveApiUrl, {
        'data': JSON.stringify(requestPayload)  // Send the payload as a JSON string
    });
});
