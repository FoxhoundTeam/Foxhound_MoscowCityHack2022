from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/moscowsityhack2022'
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    href = db.Column(db.String(250), unique=True)

    def __init__(self, name, href):
        self.name = name
        self.href = href

    def __repr__(self):
        return '<Category %r>' % self.name


class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('subcategory', lazy=True))
    href = db.Column(db.String(250), unique=True)

    def __repr__(self):
        return '<Subcategory %r>' % self.name


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), index=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    subcategory = db.relationship('Subcategory', backref=db.backref('items', lazy=True))
    href = db.Column(db.String(250), unique=True, index=True)

    def __repr__(self):
        return '<Items %r>' % self.name


class Params(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True)
    value = db.Column(db.String(500))
    units = db.Column(db.String(500))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    item = db.relationship('Items', backref=db.backref('params', lazy=True))


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    item = db.relationship('Items', backref=db.backref('brand', lazy=True))


class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.Text())
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    item = db.relationship('Items', backref=db.backref('desc', lazy=True))


db.create_all()

URL_TEMPLATE = 'https://www.wildberries.ru'


def parsing_category():
    r = requests.get(URL_TEMPLATE)
    if r.status_code == 200:
        soup = bs(r.text, "html.parser")
        categories = soup.find_all('a', class_=lambda value: value and value.startswith(
            "menu-burger__main-list-link menu-burger__main-list-link"))
        category_hrefs = {}
        for category in categories:
            category_hrefs[category.get_text()] = category['href']

        for name, href in category_hrefs.items():
            category = db.session.query(Category).filter_by(name=name).first()
            if not category:
                category = Category(name=name, href=href)
                db.session.add(category)
            else:
                category.name = name
                category.href = href

        db.session.commit()


def parsing_subcategory():
    categories = Category.query.all()
    for category in categories:
        r = requests.post(category.href)
        if r.status_code == 200:
            soup = bs(r.text, "html.parser")
            subcategory_ul = soup.find_all('ul', class_='menu-catalog__list-2')
            if subcategory_ul:
                subcategory = bs(str(subcategory_ul[0]), "html.parser")
                links = subcategory.select('ul > li > a')
                for link in links:
                    name = link.get_text()
                    href = link['href']
                    subcategory = db.session.query(Subcategory).filter_by(name=name).first()
                    if not subcategory:
                        subcategory = Subcategory(name=name, href=URL_TEMPLATE + href, category=category)
                        db.session.add(subcategory)
                    else:
                        subcategory.name = name
                        subcategory.href = URL_TEMPLATE + href

    db.session.commit()


def parsing_items():
    subcategories = Subcategory.query.all()
    count = 0
    for subcategory in subcategories:
        if subcategory.category.id < 17:
            continue
        for i in range(1, 5):
            url = subcategory.href + f'?sort=popular&page={i}'
            r = requests.post(url)
            if r.status_code == 200:
                soup = bs(r.text, "html.parser")
                items = soup.find_all('a', class_='product-card__main j-open-full-product-card')

                if not items:
                    break

                for item in items:
                    count += 1
                    if count % 100 == 0:
                        print(count, datetime.now())
                    href = URL_TEMPLATE + item['href']
                    item = db.session.query(Items).filter_by(href=href).first()
                    if not item:
                        item_db = Items(href=href, subcategory=subcategory)
                        db.session.add(item_db)
                    else:
                        item.href = href
            else:
                print('Ошибка')
                break
        db.session.commit()


def parsing_items_param():
    items = Items.query.all()
    count_items = 0
    count_params = 0
    for item in items:
        if item.name or item.subcategory.category.id < 12:
            continue
        count_items += 1
        if count_items % 100 == 0:
            print('Обьектов разобрано-', count_items, item.subcategory.category, item.subcategory, datetime.now())
        href = item.href
        try:
            article = href.split('/')[-2]
            r = requests.get(f'https://wbx-content-v2.wbstatic.net/ru/{article}.json')
            data = dict(json.loads(r.text))
            subj_name = data.get('subj_name')
            if subj_name is not None:
                param_db = Params(name='subj_name', value=subj_name, units='', item=item)
                db.session.add(param_db)
            subj_root_name = data.get('subj_root_name')
            if subj_root_name is not None:
                param_db = Params(name='subj_root_name', value=subj_root_name, units='', item=item)
                db.session.add(param_db)
            brand_name = data.get('selling', {}).get('brand_name', '')
            brand_db = Brand(name=brand_name, item=item)
            db.session.add(brand_db)
            description = data.get('description', '')
            description_db = Description(desc=description, item=item)
            db.session.add(description_db)
            item_name = data.get('imt_name', f"{brand_name}/{subj_root_name}/{subj_name}/{article}")
            item.name = item_name
            options = data.get('options', [])
            for option in options:
                count_params += 1
                if count_params % 1000 == 0:
                    print('Параметров разобрано-', count_params, datetime.now())
                name = option.get('name')
                value = option.get('value')
                units = option.get('measure', '')
                if name is not None and value is not None:
                    param_db = Params(name=name, value=value, units=units, item=item)
                    db.session.add(param_db)
        except Exception as ex:
            print('Ошибка')
            continue
        finally:
            if count_items % 1000 == 0:
                db.session.commit()
                print('коммит', datetime.now())


def create_csv():
    categories = Category.query.all()
    count = 0
    result = {
        'name': [],
        'category': [],
        'subcategory': [],
        'description': [],
        'brand': [],
        'params': []
    }
    for category in categories:
        for subcategory in category.subcategory:
            items = subcategory.items
            for item in items:
                if item.name is None:
                    continue
                count += 1
                if count % 1000 == 0:
                    print(count, datetime.now())
                params_item = ''
                for param in item.params:
                    params_item += f";{param.name}-{param.value} {param.units}"
                result['name'].append(item.name)
                result['category'].append(category.name)
                result['subcategory'].append(subcategory.name)
                result['description'].append(item.desc[0].desc)
                result['params'].append(params_item)
                result['brand'].append(item.brand[0].name)

    df = pd.DataFrame(result)
    df.to_csv('out.csv', index=True)

create_csv()

@app.route('/', methods=['POST'])
def hello_world():
    data = request.json
    method = data['method']
    result = []
    count = 0
    if method == 'get_items':
        category = data['category']
        subcategory_name = data.get('subcategory')
        name = data.get('name')
        params = data.get('params', {})
        category = Category.query.filter_by(name=category).first()
        for subcategory in category.subcategory:
            if subcategory_name is None or subcategory.name == subcategory_name:
                items = subcategory.items
                for item in items:
                    count += 1
                    if count % 1000:
                        print(count, datetime.now())
                    if name is None or item.name == name:
                        params_item = []
                        for param in item.params:
                            params_item.append({
                                'name': param.name,
                                'value': param.value,
                                'units': param.units,
                            })
                        result.append({
                            'name': item.name,
                            'params': params_item,
                            'category': category.name,
                            'subcategory': subcategory.name,
                        })

    response = app.response_class(
        response=json.dumps({'data': result}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
