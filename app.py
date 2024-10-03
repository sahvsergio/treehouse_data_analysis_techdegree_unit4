import csv
import datetime
import os
import sys
import time
from statistics import mode

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
    try:
        if qty_str.isalpha():
            raise Exception('This is not a number')


        else:
            return int(qty_str)

    except Exception as e:
        print(e)








def clean_price(price_str):
    if '$' in price_str:
        split_price = price_str.split('$')
        price_float = float(split_price[1])
    else:
        price_float = float(price_str)
    return int(price_float * 100)


# loading function
def add_csv():
    # open brands_file
    with open('brands.csv') as brands_file:
        brands = csv.DictReader(brands_file)
        # loop through the brand.csv file
        for brand in brands:
            # create a variable
            # which queries
            # whether the brand is in the database
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
                if brand_in_db.brand_name == brand['brand_name']:
                    print('This brand was already existing in the database')
                # brand names are not equal to the database
                else:
                    new_brand = Brand(brand_name=brand['brand_name'])
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
                    new_product = Product(
                        product_name=product_name,
                        product_price=product_price,
                        product_quantity=product_quantity,
                        date_updated=_date_updated,
                        brand_id=product_brand_id
                    )
                    session.add(new_product)

                session.commit()

# menu


def menu():
    '''
    Menu
    creates a menu for the application
    args:None
    Returns:str

    '''
    while True:
        print(
            '''
            Grocery Store Inventory

            \n* View a single product\'s inventory(v)
            \r*Add a new product to the database (n)
            \r*View an Analysis(a)
            \r*Make a backup of the entire inventory(b)

            ''')
        choice = input('What would you like to do?: ')
        if choice in ['v', 'n', 'a', 'b']:
            return choice
        else:
            input(
                '''
                \rPlease enter one of the options above


                \rPress enter to try again:''')
        print()


def view_product():
    try:
        product_id = int(input('Please enter the id of the product: '))
        print()
        print()
        desired_product = session.query(Product).\
            filter(Product.product_id == product_id)
        if desired_product is not None:
            for product in desired_product:
                brand_in_db = session.query(Brand).\
                    all()

                for brand in brand_in_db:
                    if brand.brand_id == product.brand_id:
                        print(f'''
                              Product Name: {product.product_name}
                              Product Quantity:{product.product_quantity} units
                              Product Price:${product.product_price/100:.2f}
                              Date last updated:{product.date_updated}
                              Brand:{brand.brand_name}
              '''
                              )
        if product_id > len(session.query(Product).all()):
            raise Exception('This  product id is not valid, please try again ')

    except ValueError:
        print(f'Please enter a valid value for the id\
            -a number from  1-{len(session.query(Product).all())}')
        view_product()
    except Exception as e:
        print()
        print(e)
        print()
        view_product()
    else:
        time.sleep(1.5)
        print('returning to the main menu')
        time.sleep(2)


def add_product():
    product_name = input('Please enter a product name')

    while True:
        try:
            product_quantity = int(input('''Please enter the quantity of the product'''))
            if product_quantity<=0:
                raise Exception('Please enter a number higher than 0')


        except ValueError:
            print('Please enter a valid value for the quantity')
        except Exception as e:
            print(e)
        else:
            break
    while True:
        try:
            product_price=float(input('Please enter the price for the unit'))
            if type(product_price)==str:
                product_price=clean_price(product_price)
            elif type(product_price)==float:
                break
            elif product_price<=0:
                raise Exception('Price cannot be lower than 0')
        except ValueError:
            print('Please enter a number not a letter')
        
            
        except Exception as e:
            print(e)
        

    brand_name = input('Please enter a brand name')
    product_in_db = session.query(Product).\
        filter(Product.product_name == product_name).\
        one_or_none()
    # if the product doesn't exist in the database
    if product_in_db is None:
        brand_in_db = session.query(Brand).\
            filter(Brand.brand_name == brand_name).\
            one_or_none()
        if brand_in_db is None:
            new_brand = Brand(brand_name=brand_name)
            session.add(new_brand)
        session.commit()

        added_product = Product(
            product_name=product_name,
            product_quantity=product_quantity,
            product_price=product_price,
            brand_id=new_brand.brand_id)
        session.add(added_product)
    session.commit()

    if product_in_db is not None:
        print('Product already in the system, updating with new details')
        product_in_db.product_price = clean_price(product_price)
        product_in_db.product_quantity = clean_quantity(product_quantity)
        product_in_db.date_updated = datetime.datetime.now()
        product_in_db.brand_id = product_in_db.brand_id

        session.commit()
    time.sleep(2)
    print('returning to main menu')
    time.sleep(2)
    

def view_analysis():
    price_list = []
    list_of_brands = []
    products = session.query(Product).all()

    for product in products:
        product_price = product.product_price
        price_list.append(product_price)
        product_brand = product.brand_id
        list_of_brands.append(product_brand)
    max_price = max(price_list)
    min_price = min(price_list)
    brand_mode = mode(list_of_brands)

    for product in products:
        if product.product_price == max_price:
            highest_product = product.product_name
        if product.product_price == min_price:
            lowest_product = product.product_name
    repeat_brand = session.query(Brand).\
        filter(Brand.brand_id == brand_mode).\
        one_or_none()

    print(f'''
          DATABASE ANALYTICS BELOW

          This is the most expensive  product in the database
          {highest_product} at ${max_price}
          This is the least expensive product in the database:
          {lowest_product} at ${min_price}
          This is the brand that has the most products in the database:
          {repeat_brand.brand_name}

          ''')
    time.sleep(2)
    print('returning to main menu')
    time.sleep(2)


def create_backup():
    "creates 2 backup files"
    with open('backup_inventory.csv', 'w') as backup_inventory:
        inventory_fields = [
            'product_id',
            'product_name',
            'product_quantity',
            'product_price',
            'date_updated',
            'brand_id'


            ]
        data = session.query(Product).all()
        inventory_backer = csv.DictWriter(
            backup_inventory, fieldnames=inventory_fields)
        inventory_backer.writeheader()
        for datum in data:
            inventory_backer.writerow(
                {
                    'product_id': datum.product_id,
                    'product_name': datum.product_name,
                    'product_quantity': datum.product_quantity,
                    'product_price': datum.product_price,
                    'date_updated': datum.date_updated,
                    'brand_id': datum.brand_id
                }
            )
    with open('backup_brands.csv', 'w') as backup_brands:
        brand_fields = [
            'brand_id',
            'brand_name'
        ]
        brand_data = session.query(Brand).all()
        brand_backer = csv.DictWriter(
            backup_brands, fieldnames=brand_fields)
        brand_backer.writeheader()
        for brand_datum in brand_data:
            brand_backer.writerow(

                {'brand_id': brand_datum.brand_id,
                 'brand_name':brand_datum.brand_name
                 }
                )
            
            
           


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
    while app_running:
        choice = menu()

        if choice == 'v':
            # view a single product
            view_product()
        elif choice == 'a':
            view_analysis()

            # analyze()

        elif choice == 'n':
            # add a product
            add_product()

        elif choice == 'b':
            # create backup
            create_backup()

        else:
            app_running = False
            input(
                '''
                \rPlease enter one of the options above
                \rletters a, b or v only
                \rPress enter to try again:
                ''')
        print('Thank you for using our system, good bye ')

    # sys.exit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
