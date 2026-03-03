import re
import json

def normalize_price(price_str):
    return float(price_str.replace(" ", "").replace(",", "."))
def ab(test):
    pattern=r"ab*"
    res=re.findall(pattern,test)
    return res
def  a_b_2_3(test):
    pattern=r"ab{2,3}"
    res=re.findall(pattern,test)
    return res
def  lower(test):
     pattern = r"\b[a-z]+_[a-z]+\b"
     text = "hello_world test_var Wrong_Var"
     matches = re.findall(pattern, text)
def a_b(test):
    pattern = r"a.*b"
    text = "a123b axxb aXb ab"
    matches = re.findall(pattern, text)
def rep(test):
      text = "Hello, world. Python is fun"
      result = re.sub(r"[ ,\.]", ":", text)
      print(result)
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)

with open(r"C:\Users\User\Desktop\Practice Python\PracticePP2\Practice5\Raw.txt", "r", encoding="utf-8") as f:
    text = f.read()


price_pattern = r"\d[\d ]*,\d{2}"
all_prices_raw = re.findall(price_pattern, text)
all_prices = [normalize_price(p) for p in all_prices_raw]


product_pattern = r"\d+\.\n(.+)"
product_names = re.findall(product_pattern, text)




item_total_pattern = r"x [\d ]+,\d{2}\n([\d ]+,\d{2})"
item_totals_raw = re.findall(item_total_pattern, text)
item_totals = [normalize_price(t) for t in item_totals_raw]

calculated_total = sum(item_totals)



datetime_pattern = r"Время:\s(\d{2}\.\d{2}\.\d{4})\s(\d{2}:\d{2}:\d{2})"
datetime_match = re.search(datetime_pattern, text)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None



payment_pattern = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_pattern, text)

payment_method = payment_match.group(1) if payment_match else None


result = {
    "product_names": product_names,
    "all_prices": all_prices,
    "calculated_total": calculated_total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(result, ensure_ascii=False, indent=4))