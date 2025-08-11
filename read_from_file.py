def read_login_password(filename="login.txt"):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        email = lines[0].strip()
        password = lines[1].strip()
        return email, password
    
def read_products(filename="products.txt"):
    products = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or ',' not in line:
                continue
            product_id, code = line.split(",", 1)
            products.append({"PRODUCT_ID": product_id.strip(), "CODE": code.strip()})
    return products