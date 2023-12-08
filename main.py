import sqlite3
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
def remove_rating_info(product_list):  # product rating info excluded from the related class
    return [item for item in product_list if "5 üzerinden" not in item]

product=input("Enter product name: ")

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.eminonuboncuk.com/")
search= driver.find_element(By.NAME,"s")
search.send_keys(product)
search.submit()

try:
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "product-small")))
except TimeoutException:
    print("there is no related product listed yet")
    driver.quit()

products = []
seen_boxes = set()

while True:
    boxes = driver.find_elements(By.CLASS_NAME, "box")
    new_boxes = [box for box in boxes if box not in seen_boxes]
    if not new_boxes:
        break

    for box in new_boxes:
        product_details = box.text.split('\n')
        product_details = remove_rating_info(product_details)
        products.append(product_details)
        seen_boxes.add(box)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.CLASS_NAME, "box")) > len(boxes))
    except TimeoutException:
        print("Finished")
        break

driver.quit()

print(f"Toplam ürün sayısı: {len(products)}")
for product in products[:5]:
    print(product)

conn = sqlite3.connect('mydatabase.db')

c= conn.cursor()

#c.execute("DELETE FROM table_sample_boncuk")

c.execute("""CREATE TABLE IF NOT EXISTS table_sample_boncuk (
category text,
name text,
price integer)""")

conn.cursor()
for product in products:

    if len(product) == 3:
        price_str = product[2].replace('₺', '').replace(',', '.')
        if '–' in price_str: # some prices being showed with two integers . like '20-30 Turkish liras '
            prices = price_str.split('–')

            min_price = float(prices[0].strip())

            max_price = float(prices[1].strip())

            price = int((min_price+max_price)/2)  # i take average of both prices
        else:
            price = int(float(price_str))

        c.execute("INSERT INTO table_sample_boncuk (category, name, price) VALUES (?, ?, ?)", (product[0], product[1], price))

    else:
        print(f"Skipping a product due to missing data: {product}")

c.execute("SELECT * FROM table_sample_boncuk")

rows = c.fetchall()

with open('output.csv', 'w', newline = '', encoding='utf-8') as f:

    writer = csv.writer(f)

    writer.writerow([i[0] for i in c.description])

    writer.writerows(rows)

conn.close()