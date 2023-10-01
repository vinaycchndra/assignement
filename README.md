# Test cases are written in app/tests.py files for all the methods Post(create), Get(read), Put(update), Delete(delete)
# If one wants to remove an item from the invoice, the quantity should be set zero for that item and it will automatically get deleted.
# New item can also be added in the update request those will also be added corresponding to the 'pk' for the invoice, however the description field is mandatory while adding a new item with update(Put) method.
# This is one json format format for testing the APIs manully {
    "invoice_customer_name": "Vinay Chandra Joshi",
    "item_details": [
        {
            "description": "Apples",
            "quantity": 5,
            "unit_price": "2.50",
            "price": "12.50"
        },
        {
            "description": "Bread",
            "quantity": 3,
            "unit_price": "2.00",
            "price": "8.00"
        },
        {
            "description": "Milk",
            "quantity": 1,
            "unit_price": "3.50",
            "price": "3.50"
        },
        {
            "description": "Pasta",
            "quantity": 3,
            "unit_price": "0.00",
            "price": "3.00"
        },
        {
            "description": "Roti",
            "quantity": 1,
            "unit_price": "0",
            "price": "17.00"
        },

        {
            "description": "Potato",
            "quantity": 1,
            "unit_price": "150",
            "price": "17.00"
        }

    ]
}
