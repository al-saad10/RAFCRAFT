



$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var quantityElement = $(this).closest('td').find('.quantity');
    $.ajax({
        type: "GET",
        url: "/plus-cart",
        data: {
            prod_id: id
        },
        success: function(data) {
            quantityElement.text(data.quantity);
            $('#amount').text(data.amount);
            $('#totalamount').text(data.totalamount);
        }
    });
});


$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var quantityElement = $(this).closest('td').find('.quantity');
    $.ajax({
        type: "GET",
        url: "/minus-cart",
        data: {
            prod_id: id
        },
        success: function(data) {
            quantityElement.text(data.quantity);
            $('#amount').text(data.amount);
            $('#totalamount').text(data.totalamount);
        }
    });
});

$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type: "GET",
        url: "/remove-cart",
        data: {
            prod_id: id
        },
        success: function(data) {
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            $(eml).closest('tr').remove(); // Remove the closest <tr> element
            // Check if cart is empty
            if (data.totalamount === 0) {
                // Redirect to the empty cart page
                window.location.href = "/cart";
            }
        }
    });
});

function toggleDropdown(dropdownId) {
    var dropdownMenu = document.getElementById(dropdownId);
    dropdownMenu.style.display = "block";
}

function closeDropdown(dropdownId) {
    var dropdownMenu = document.getElementById(dropdownId);
    dropdownMenu.style.display = "none";
}

function keepDropdownOpen(dropdownId) {
    var dropdownMenu = document.getElementById(dropdownId);
    dropdownMenu.style.display = "block";
} 

// single product slider

var MainImg = document.getElementById("MainImg");
var smallimg = document.getElementsByClassName("small-img");

for (var i = 0; i < smallimg.length; i++) {
    smallimg[i].onclick = function() {
        MainImg.src = this.src;
    };
}