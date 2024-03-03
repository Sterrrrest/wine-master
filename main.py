import datetime
import pandas
import collections
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler

excel_data_df2 = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', na_values=['N/A','NA'], keep_default_na=False)
items = excel_data_df2.to_dict('records')
categories = collections.defaultdict(list)
products = collections.defaultdict(list)
prices = collections.defaultdict(list)

for item in items:
    products[item['Категория']].append(item)
    prices[item['Цена']].append(item['Цена'])

min_price = min(prices)

foundation_year = datetime.datetime(year=1920, month=1, day=1, hour=0)
today = datetime.datetime.today()
old_duration = (today - foundation_year).days // 365
last_digit = (str(old_duration)[-1])

if (last_digit == '2' or last_digit == '3' or last_digit == '4') and (str(old_duration)[-2] != '1'):
    print(old_duration, 'года')
elif (last_digit == '1') and (int(str(old_duration)[-2]) != 1):
    print(old_duration, 'год')
else:
    print(old_duration, 'лет')


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    duration=old_duration, items=items, products=products, min_price=min_price
)

with open('template.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
