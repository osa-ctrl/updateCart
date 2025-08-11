import requests
from bs4 import BeautifulSoup
import json

def read_urls_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def read_cookies(filename="cookies.json"):
    with open(filename, "r") as f:
        cookies = json.load(f)
    return {cookie['name']: cookie['value'] for cookie in cookies}

def parse_product_info(url, cookies):
    try:
        resp = requests.get(url, cookies=cookies, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Парсим <span id="productCode">
        code_elem = soup.find('span', id='productCode')
        code = code_elem.text.strip() if code_elem else None

        # Парсим <input type="hidden" name="product" value="...">
        prod_elem = soup.find('input', {'name': 'product'})
        product_id = prod_elem['value'].strip() if prod_elem else None

        if product_id and code:
            return {"PRODUCT_ID": product_id, "CODE": code}
        else:
            return None
    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")
        return None

def main():
    urls = read_urls_from_file("urls.txt")
    cookies = read_cookies("cookies.json")
    products = []
    for url in urls:
        info = parse_product_info(url, cookies)
        if info:
            print(f"Найдено: {info}")
            products.append(info)
        else:
            print(f"Не удалось получить данные для {url}")

    # Сохраняем в products.txt
    with open("products.txt", "w") as f:
        for prod in products:
            f.write(f"{prod['PRODUCT_ID']},{prod['CODE']}\n")
    print("Готово! Данные сохранены в products.txt")

if __name__ == "__main__":
    main()