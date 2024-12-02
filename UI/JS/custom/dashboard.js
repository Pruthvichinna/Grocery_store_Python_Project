$(function () {
    // Fetch order data from the API using GET request
    $.get(orderListApiUrl, function (response) {
        if (response) {
            var table = '';  // Initialize an empty string to hold the table rows
            var totalCost = 0;  // Initialize a variable to keep track of the total cost

            // Iterate through each order in the response data
            $.each(response, function(index, order) {
                totalCost += parseFloat(order.total);  // Add the order total to the total cost
                table += '<tr>' +  // Start a new row for each order
                    '<td>' + order.datetime + '</td>' +  // Display order datetime
                    '<td>' + order.order_id + '</td>' +  // Display order ID
                    '<td>' + order.customer_name + '</td>' +  // Display customer name
                    '<td>' + order.total.toFixed(2) + ' Rs</td></tr>';  // Display total cost formatted to 2 decimal places
            });

            // Add a row for the grand total cost at the bottom of the table
            table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>' + totalCost.toFixed(2) + ' Rs</b></td></tr>';
            
            // Update the table body with the new rows (this will replace the old rows)
            $("table").find('tbody').empty().html(table);
        }
    });
});
