import csv
import datetime
import os
import sys
import time


# Related third-party imports
from models import Base, session, Product, Brand, engine


# cleaning functions

def clean_date(date_str):
    '''Turns the string into a date object'''

    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])

    return datetime.date(year, month, day)


def clean_quantity(qty_str):

    return int(qty_str)


def clean_price(price_str):
    if '$' in price_str:
        split_price = price_str.split('$')
        price_float = float(split_price[1])
    else:
        price_float = float(price_str)
    return int(price_float * 100)

# loading 


def add_csv():
    # open brands_file
    with open('brands.csv') as brands_file:
        brands = csv.DictReader(brands_file)
        # loop through the brand.csv file
        for brand in brands:
            # create a variable which queries whether the brand is in the database
            brand_in_db = session.query(Brand).\
                filter(Brand.brand_name == brand['brand_name']).\
                one_or_none()
            # if database is empty
            if brand_in_db is None:
                # save the brand name
                brand_name = brand['brand_name']
                # create a new instance of the brand with the new brand name
                new_brand = Brand(brand_name=brand_name)
                # add it to the session
                session.add(new_brand)
            # commit changes
            session.commit()
            # if database has any content
            if brand_in_db is not None:
                # if brand names in database are equal to  the ones in csv file
                if brand_in_db.brand_name==brand['brand_name']:
                    print('This brand was already existing in the database')
                #brand names are not equal to the database    
                else:
                    new_brand=Brand(brand_name=brand['brand_name'])
                    session.add(new_brand)
                session.commit()
              
               
                   
                    


    with open('inventory.csv') as inventory_file:
        products = csv.DictReader(inventory_file)
        for product in products:
            product_name = product['product_name']
            product_price = clean_price(product['product_price'])
            product_quantity = clean_quantity(product['product_quantity'])
            _date_updated = clean_date(product['date_updated'])
            product_brand = product['brand_name']
            brand_in_db = session.query(Brand).\
                all()
            for brand in brand_in_db:
                if brand.brand_name == product['brand_name']:
                    product_brand_id = brand.brand_id
                    new_product=Product(
                        product_name=product_name,
                        product_price=product_price,
                        product_quantity=product_quantity,
                        date_updated=_date_updated,
                        brand_id=product_brand_id
                    )
                    session.add(new_product)

                session.commit()





def app():
    try:
        add_csv()
    except (FileNotFoundError):
        print()
        print()
        print('No source csv found, please review')
        print()
        print()

    app_running = True


if __name__ == '__main__':

    Base.metadata.create_all(engine)
    app()
