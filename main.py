import datetime
import pandas
import collections
import argparse
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler
from environs import Env

FOUNDATION_DATE = 1920

if __name__ == '__main__':
    environment = Env()
    environment.read_env()
    parser = argparse.ArgumentParser(description='Программа обрабатывает exl файл и выгружает данные на сайт')
    parser.add_argument('-f', '--file_name', help='Имя файла', default=environment('FILE_NAME'))
    parser.add_argument('-l', '--file_list', help='Название страницы', default=environment('SHEET_NAME'))
    args = parser.parse_args()
    excel_data_df2 = pandas.read_excel(args.file_name, sheet_name=args.file_list, na_values=['N/A','NA'], keep_default_na=False)

    file_db = excel_data_df2.to_dict('records')
    products = collections.defaultdict(list)

    for item in file_db:
        products[item['Категория']].append(item)

    age = datetime.datetime.today().year - FOUNDATION_DATE
    last_digit = (str(age)[-1])
    if (last_digit == '2' or last_digit == '3' or last_digit == '4') and (str(age)[-2] != '1'):
        age = f"{age} года"
    elif (last_digit == '1') and (int(str(age)[-2]) != 1):
        age = f"{age} год"
    else:
        age = f"{age} лет"

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        products=products, age=age
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
