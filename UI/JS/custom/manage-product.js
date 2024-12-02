// Define a reference to the product modal for easy access
var productModal = $("#productModal");

$(function () {
    // Fetch the product list from the API when the page is loaded
    $.get(productListApiUrl, function (response) {
        if (response) {
            var table = '';  // Initialize an empty string to store table rows
            $.each(response, function(index, product) {
                // For each product, create a table row with product details
                table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.uom_id +'" data-price="'+ product.price_per_unit +'">' +
                    '<td>'+ product.name +'</td>'+  // Display product name
                    '<td>'+ product.uom_name +'</td>'+  // Display unit of measurement
                    '<td>'+ product.price_per_unit +'</td>'+  // Display price per unit
                    '<td><span class="btn btn-xs btn-danger delete-product">Delete</span></td></tr>';  // Delete button for the product
            });
            // Update the table body with the generated rows
            $("table").find('tbody').empty().html(table);
        }
    });
});

// Event handler for saving a new product
$("#saveProduct").on("click", function () {
    // Serialize the form data into an array
    var data = $("#productForm").serializeArray();
    
    // Initialize the request payload with null values
    var requestPayload = {
        product_name: null,
        uom_id: null,
        price_per_unit: null
    };

    // Loop through form data and assign values to the payload
    for (var i = 0; i < data.length; ++i) {
        var element = data[i];
        switch (element.name) {
            case 'name':
                requestPayload.product_name = element.value;  // Set product name
                break;
            case 'uoms':
                requestPayload.uom_id = element.value;  // Set UOM ID
                break;
            case 'price':
                requestPayload.price_per_unit = element.value;  // Set price per unit
                break;
        }
    }

    // Call API to save the new product with the serialized data
    callApi("POST", productSaveApiUrl, {
        'data': JSON.stringify(requestPayload)  // Send the data as a JSON string
    });
});

// Event handler for deleting a product
$(document).on("click", ".delete-product", function () {
    var tr = $(this).closest('tr');  // Find the closest row to the clicked delete button
    var data = {
        product_id: tr.data('id')  // Get product ID from the row data attribute
    };
    
    // Confirm with the user before deleting
    var isDelete = confirm("Are you sure to delete " + tr.data('name') + " item?");
    if (isDelete) {
        // If confirmed, call the API to delete the product
        callApi("POST", productDeleteApiUrl, data);
    }
});

// Event handler for when the product modal is hidden (reset form)
productModal.on('hide.bs.modal', function(){
    // Reset the form fields
    $("#id").val('0');
    $("#name, #unit, #price").val('');  // Clear the input fields
    productModal.find('.modal-title').text('Add New Product');  // Reset the modal title
});

// Event handler for when the product modal is shown (populate UOM dropdown)
productModal.on('show.bs.modal', function(){
    // Fetch the list of UOMs from the API when the modal is shown
    $.get(uomListApiUrl, function (response) {
        if (response) {
            var options = '<option value="">--Select--</option>';  // Initialize a default "Select" option
            $.each(response, function(index, uom) {
                // Append each UOM to the options list
                options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
            });
            // Update the UOM dropdown with the fetched options
            $("#uoms").empty().html(options);
        }
    });
});
