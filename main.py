import requests
import json
import time
import random
from save_cookies import save_cookies
from read_from_file import read_login_password, read_products

EMAIL, PASSWORD = read_login_password("login.txt")

PRODUCTS = read_products("products.txt")

COOKIES_FILE = "cookies.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Referer": "https://www.bestsecret.com/entrance/index.htm",
    "Content-Type": "application/json"
}

def load_cookies():
    try:
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)
        jar = requests.cookies.RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'], domain='www.bestsecret.com')
            jar.set(cookie['name'], cookie['value'], domain='www.bestsecret.at')
            jar.set(cookie['name'], cookie['value'], domain='.bestsecret.com')
            jar.set(cookie['name'], cookie['value'], domain='.bestsecret.at')
        return jar
    except FileNotFoundError:
        save_cookies(EMAIL, PASSWORD, COOKIES_FILE)
        return load_cookies()
    except json.JSONDecodeError:
        print("🔴 Ошибка чтения файла cookies.json. Проверьте формат.")
        return None

def add_to_cart(product):
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies = load_cookies()
    add_url = f"https://www.bestsecret.com/add_to_cart.ujs?product={product['PRODUCT_ID']}&category=&doubleClickPreventorAddToCart={int(time.time()*1000)}&recommended=&area=&back_url=%2Fentrance%2Findex.htm&activeProductImageIndex=0&code={product['CODE']}&quantity=1"
    resp = session.get(add_url)
    if resp.status_code == 200:
        print(f"🟢 Товар {product['PRODUCT_ID']} добавлен в корзину!")
        return True
    else:
        print(f"🔴 Ошибка добавления {product['PRODUCT_ID']}: {resp.status_code} — {resp.text[:200]}")
        return False

def remove_from_cart(product):
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies = load_cookies()
    payload = {
        "operationName": "ChangeProductQuantityInCart",
        "variables": {
            "productCode": product['CODE'],
            "quantity": 0
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "96e802300cb23d07c96d9281c02d1364f7891a28bd370de47871fd0983086f71"
            }
        }
    }
    resp = session.post("https://www.bestsecret.at/bff-spa", data=json.dumps(payload))
    if resp.status_code == 200 and '"errors":' not in resp.text:
        print(f"🟢 Товар {product['PRODUCT_ID']} удалён из корзины!")
        return True
    else:
        print(f"🔴 Ошибка удаления {product['PRODUCT_ID']}: {resp.status_code} — {resp.text[:200]}")
        return False

if __name__ == "__main__":
    while True:
        product = random.choice(PRODUCTS)
        print(f"▶️ Работаем с товаром: {product['PRODUCT_ID']}")
        success_add = add_to_cart(product)
        if not success_add:
            print("⏩ Пробуем следующий товар...")
            continue
        success_remove = remove_from_cart(product)
        if not success_remove:
            print("⏩ Пробуем следующий товар...")
            continue
        delay = random.randint(600, 1200)
        print(f"⏳ Жду {delay // 60} мин {delay % 60} сек до следующего цикла...")
        time.sleep(delay)