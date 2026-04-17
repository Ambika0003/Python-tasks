import numpy as np

# user adds items to a shopping cart and Store items in a list
cart=("Apple","Orange","Milk","Water","Glass","Pen","Soap","Apple","Pen","Milk")
print(list(cart))

#Convert to set to remove duplicates 
new_cart=set(list(cart))
print("the cart after removing duplicates:\n",new_cart)

#Use loop + condition to calculate total cost 
prices={"Apple":50,"Orange":40,"Milk":15,"Water":10,"Glass":60,"Pen":5,"Soap":25}
total=0
for item in new_cart:
    try:
        item_lower=item.lower()

        if item in prices:
            total+=prices[item]
        else:
            raise ValueError("Item is not available in price list")
    except ValueError as e:
        print("Error",e)

print("total cost of the cart is :\n", total)

