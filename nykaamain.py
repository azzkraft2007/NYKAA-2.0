import mysql.connector as sqltor

def connect_to_nykaa_database():
    try:
        mycon = sqltor.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="NYKAA")
        if mycon.is_connected():
            print("Connection to the NYKAA database successful!")
            return mycon
        else:
            print("Error connecting to the NYKAA database")
            return None
    except sqltor.Error as err:
        print(f"Error: {err}")
        return None

def admin_login():
    username = "nykaa admin"
    password = "nykaa1234"
    userinput_username= input("Enter Username: ")
    if userinput_username.lower() == username:
        userinput_password = input("Enter Password: ")
        if userinput_password == password:
            print("Login Successful! Welcome Admin")
            return True
        else:
            print("Incorrect password. Try again.")
            return False
    else:
        print("Incorrect username. Try again.")
        return False

def manage_products(cur, mycon):
    print("\nProduct Management")
    print("1. Add Product")
    print("2. Update Product")
    print("3. Remove Product")
    product_choice = int(input("Enter your choice (1-3): "))
    if product_choice == 1:
        product_name = input("Enter product name: ")
        product_category = input("Enter product category: ")
        product_description = input("Enter product description: ")
        brand_id = int(input("Enter brand ID: "))
        product_price = float(input("Enter product price: "))
        product_stock = int(input("Enter stock quantity: "))
        query = "INSERT INTO products (product_name, category, product_description, brand_id, price, stock) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (product_name, product_category, product_description, brand_id, product_price, product_stock))
        mycon.commit()
        print(f"Product '{product_name}' added with price {product_price} and stock {product_stock}")
    elif product_choice == 2:
        product_id = int(input("Enter product ID to update: "))
        new_price = float(input("Enter new price: "))
        new_stock = int(input("Enter new stock quantity: "))
        query = "UPDATE products SET price = %s, stock = %s WHERE product_id = %s"
        cur.execute(query, (new_price, new_stock, product_id))
        mycon.commit()
        print(f"Product {product_id} updated with new price {new_price} and new stock {new_stock}")
    elif product_choice == 3:
        product_id = int(input("Enter product ID to remove: "))
        query = "DELETE FROM products WHERE product_id = %s"
        cur.execute(query, (product_id,))
        mycon.commit()
        print(f"Product {product_id} removed from the inventory")

def manage_customers(cur, mycon):
    print("\nCustomer Management")
    print("1. View All Customers")
    print("2. Add New Customer")
    print("3. Remove Customer")
    customer_choice = int(input("Enter your choice (1-3): "))
    if customer_choice == 1:
        query = "SELECT * FROM customers"
        cur.execute(query)
        customers = cur.fetchall()
        print("Customers List:")
        for customer in customers:
            print(customer)
    elif customer_choice == 2:
        first_name = input("Enter customer first name: ")
        last_name = input("Enter customer last name: ")
        address = input("Enter customer address: ")
        email_id = input("Enter customer email: ")
        phone_number = input("Enter customer phone number: ")
        dob = input("Enter customer date of birth (YYYY-MM-DD): ")
        gender = input("Enter customer gender: ")
        password = input("Create a password for the customer: ")
        query = "INSERT INTO customers (first_name, last_name, address, email_id, phone_number, dob, gender, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (first_name, last_name, address, email_id, phone_number, dob, gender, password))
        mycon.commit()
        print(f"Customer '{first_name} {last_name}' added.")
    elif customer_choice == 3:
        customer_id = int(input("Enter customer ID to remove: "))
        query = "DELETE FROM customers WHERE NYKID = %s"
        cur.execute(query, (customer_id,))
        mycon.commit()
        print(f"Customer {customer_id} removed from the database")

def manage_orders(cur, mycon):
    print("\nOrder Management")
    print("1. View All Orders")
    print("2. Update Order Status")
    print("3. Remove Order")
    order_choice = int(input("Enter your choice (1-3): "))
    if order_choice == 1:
        query = "SELECT * FROM orders"
        cur.execute(query)
        orders = cur.fetchall()
        print("Orders List:")
        for order in orders:
            print(order)
    elif order_choice == 2:
        order_id = int(input("Enter order ID to update: "))
        new_status = input("Enter new order status (e.g., Shipped, Delivered): ")
        query = "UPDATE orders SET order_status = %s WHERE order_id = %s"
        cur.execute(query, (new_status, order_id))
        mycon.commit()
        print(f"Order {order_id} status updated to {new_status}")
    elif order_choice == 3:
        order_id = int(input("Enter order ID to remove: "))
        query = "DELETE FROM orders WHERE order_id = %s"
        cur.execute(query, (order_id,))
        mycon.commit()
        print(f"Order {order_id} removed from the system")

def admin_dashboard(cur, mycon):
    while True:
        print("\nAdmin Dashboard")
        print("1. Manage Products")
        print("2. Manage Customers")
        print("3. Manage Orders")
        print("4. Logout")
        choice = int(input("Enter your choice (1-4): "))
        if choice == 1:
            manage_products(cur, mycon)
        elif choice == 2:
            manage_customers(cur, mycon)
        elif choice == 3:
            manage_orders(cur, mycon)
        elif choice == 4:
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def brand_login(cur, mycon):
    print("Brand Login")
    brand_email = input("Enter Brand Email: ")
    brand_password = input("Enter Brand Password: ")
    query = "SELECT * FROM BRANDS WHERE email = %s"
    cur.execute(query, (brand_email,))
    brand_data = cur.fetchone()
    if brand_data:
        if brand_password == brand_data[3]:
            print("Login successful!")
            brand_dashboard(cur, brand_data, mycon)
        else:
            print("Invalid password. Please try again.")
    else:
        print("Invalid email. Please try again.")

def brand_dashboard(cur, brand_data, mycon):
    while True:
        print("\nBrand Dashboard")
        print("1. View My Products")
        print("2. Add New Product")
        print("3. Update Product Stock")
        print("4. Update Order Status")
        print("5. Log out")
        choice = int(input("Enter your choice (1-5): "))
        if choice == 1:
            view_products(cur, brand_data)
        elif choice == 2:
            add_product(cur, brand_data, mycon)
        elif choice == 3:
            update_product_stock(cur, brand_data, mycon)
        elif choice == 4:
            update_order_status(cur, brand_data, mycon)
        elif choice == 5:
            print("Logging out")
            break
        else:
            print("Invalid choice. Please try again.")

def view_products(cur, brand_data):
    query = "SELECT * FROM products WHERE brand_id = %s"
    cur.execute(query, (brand_data[0],))
    products = cur.fetchall()
    if products:
        for row in products:
            product_id, product_name, category, description, brand_id, stock, price = row
            print(f"ID:{product_id}, Name:{product_name}, Category:{category}, Description:{description}, Stock:{stock}, Price:{price}")
    else:
        print("No products found for this brand.")

def add_product(cur, brand_data, mycon):
    product_name = input("Enter Product Name: ")
    category = input("Enter Product Category: ")
    product_description = input("Enter Product Description(Expiry Date, Quantity, Features, etc.): ")
    stock = int(input("Enter Stock Quantity: "))
    price = float(input("Enter Product Price: "))
    query = "INSERT INTO products (product_name, category, product_description, brand_id, stock, price) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(query, (product_name, category, product_description, brand_data[0], stock, price))
    mycon.commit()
    print("Product added successfully!")

def brands_login_or_registration(cur, mycon):
    print("Brand Login or Registration")
    print("1. Login as Existing Brand")
    print("2. Register as New Brand")
    brand_option = int(input("Enter your choice (1-2): "))
    if brand_option == 1:
        brand_login(cur, mycon)
    elif brand_option == 2:
        brand_registration(cur, mycon)
    else:
        print("Invalid choice. Please try again.")



def register_customer(cur, mycon):
    print("\nCustomer Registration Form")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    address = input("Enter Address: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone Number: ")
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    gender = input("Enter Gender: ")
    password = input("Create a Password: ")
    query = "INSERT INTO customers (first_name, last_name, address, email_id, phone_number, dob, gender, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(query, (first_name, last_name, address, email, phone, dob, gender, password))
    mycon.commit()
    print(f"Customer '{first_name} {last_name}' registered successfully.")

def login_customer(cur, mycon):
    customer_email = input("Enter Email: ")
    customer_password = input("Enter Password: ")
    query = "SELECT * FROM customers WHERE email_id = %s AND password = %s"
    cur.execute(query, (customer_email, customer_password))
    customer_data = cur.fetchone()
    if customer_data:
        print("\nLogin successful! Welcome,", customer_data[1], customer_data[2])
        customer_dashboard(customer_data[0], cur, mycon)
    else:
        print("Invalid email or password. Please try again.")

def customer_login_or_registration(cur, mycon):
    print("\nCustomer Login or Registration")
    print("1. Login as Existing Customer")
    print("2. Register as New Customer")
    customer_option = int(input("Enter your choice (1-2): "))
    if customer_option == 1:
        login_customer(cur, mycon)
    elif customer_option == 2:
        register_customer(cur, mycon)
    else:
        print("Invalid choice.")


def update_skin_profile(cur, customer_id, mycon):
    print("\nUpdate Your Skin Profile")
    valid_skin_types = {"dry", "oily", "combination", "sensitive"}
    skin_type = input("Enter skin type (dry/oily/combination/sensitive): ").strip().lower()
    while skin_type not in valid_skin_types:
        skin_type = input("Invalid skin type. Enter again (dry/oily/combination/sensitive): ").strip().lower()
    sensitivities = input("Enter comma-separated ingredient sensitivities (or leave blank): ").strip().lower()
    cur.execute("SELECT * FROM skin_profiles WHERE Nykid=%s", (customer_id,))
    profile = cur.fetchone()
    if profile:
        cur.execute("UPDATE skin_profiles SET SkinType=%s, Sensitivities=%s WHERE Nykid=%s",
                    (skin_type, sensitivities, customer_id))
    else:
        cur.execute("INSERT INTO skin_profiles (Nykid, SkinType, Sensitivities) VALUES (%s, %s, %s)",
                    (customer_id, skin_type, sensitivities))
    mycon.commit()
    print("Your skin profile has been updated.")

def recommend_products(cur, customer_id):
    cur.execute("SELECT SkinType, Sensitivities FROM skin_profiles WHERE Nykid=%s", (customer_id,))
    profile = cur.fetchone()
    if not profile:
        print(" No skin profile found. Please set it up first.")
        return
    skin_type, sensitivities = profile
    sensitivity_list = [s.strip().lower() for s in sensitivities.split(',') if s.strip()] if sensitivities else []
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    # Fetch all ingredients for each product
    cur.execute("SELECT ProductID, IngrediantName FROM Ingrediants_Produ")
    ingredients_map = {}
    for pid, name in cur.fetchall():
        ingredients_map.setdefault(pid, set()).add(name.lower())
    recommended = []
    for product in products:
        product_id = product[0]
        prod_ingredients = ingredients_map.get(product_id, set())
        if not any(sens in prod_ingredients for sens in sensitivity_list):
            recommended.append(product)
    if recommended:
        print(f"\nRecommended Products for your {skin_type} skin, with sensitivities {sensitivity_list if sensitivity_list else 'None'}:")
        for prod in recommended:
            print(f"ID: {prod[0]}, Name: {prod[1]}, Category: {prod[2]}, Price: ₹{prod[5]}, Stock: {prod[6]}")
    else:
        print("No products matched your profile safely.")

def ingredient_compatibility_checker(cur, customer_id):
    cur.execute("SELECT Sensitivities FROM skin_profiles WHERE Nykid=%s", (customer_id,))
    profile = cur.fetchone()
    if not profile:
        print("No skin profile found. Please set it up first.")
        return
    sensitivities = profile[0]
    sensitivity_list = [s.strip().lower() for s in sensitivities.split(',') if s.strip()] if sensitivities else []
    if not sensitivity_list:
        print("You do not have any ingredient sensitivities set.")
        return
    product_id = int(input("Enter Product ID to check: "))
    cur.execute("SELECT IngrediantName FROM Ingrediants_Produ WHERE ProductID=%s", (product_id,))
    ingredients = [row[0].lower() for row in cur.fetchall()]
    matched = [s for s in sensitivity_list if s in ingredients]
    if matched:
        print(f"⚠️ This product contains your sensitive ingredients: {', '.join(matched)}.")
    else:
        print("✅ This product does not contain any of your sensitive ingredients.")


def customer_dashboard(customer_id, cur, mycon):
    while True:
        print("\nCustomer Dashboard")
        print("1. View Products")
        print("2. Place an Order")
        print("3. View My Orders")
        print("4. Update Profile")
        print("5. Update Skin Profile")
        print("6. Get Product Recommendations (by Skin Profile)")
        print("7. Ingredient Compatibility Checker")
        print("8. Logout")
        choice = int(input("Enter your choice (1-8): "))
        if choice == 1:
            view_products_cust(cur)
        elif choice == 2:
            place_order(cur, customer_id, mycon)
        elif choice == 3:
            view_orders(cur, customer_id)
        elif choice == 4:
            update_profile(cur, customer_id, mycon)
        elif choice == 5:
            update_skin_profile(cur, customer_id, mycon)
        elif choice == 6:
            recommend_products(cur, customer_id)
        elif choice == 7:
            ingredient_compatibility_checker(cur, customer_id)
        elif choice == 8:
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    mycon = connect_to_nykaa_database()
    if mycon:
        cur = mycon.cursor()
        print("Welcome to Nykaa!")
        login = int(input("Login as 1. Admin (enter 1) 2. Brands (enter 2) 3. Customers (enter 3): "))
        if login == 1:
            if admin_login():
                admin_dashboard(cur, mycon)
            mycon.close()
        elif login == 2:
            brands_login_or_registration(cur, mycon)
            mycon.close()
        elif login == 3:
            customer_login_or_registration(cur, mycon)
            mycon.close()
        else:
            print("Invalid login type.")
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()

 

