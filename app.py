'''Store Inventory App

This script allows the user to:

-Initializes a Sqlite database
-Creates a database model called Product
-Connect the database and create tables
-Reads in the existing CSV data
-Cleans up the data before adding each product from the csv
-Adds the data from CSV into the database
-Creates a Menu to make selections
-Displays a product by its ID - Menu Option V
-Manually Adds a new product to the database - Menu Option A
- Backups the database (Export new CSV) - Menu Option B
-Include only production-ready files in the repo


This tool accepts comma separated value files(.csv)
as manual entry for adding product

This script requires that `pandas` be installed within the Python
environment you are running this script in .

contains the following
functions:

    * menu: creates a menu for the script
    *view_product: shows product
    *add_product
    *create_backup
    *clean_date
    *clean_quantity
    *clean_price
    *add_csv
    *app
    *main - the main function of the script
'''
# Standard library imports
import csv
import datetime
import os
import sys
import time


# Related third-party imports
from models import Base, session, Product, engine




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
            Store Inventory

            \n* View a single product\'s inventory(v)
            \r*Add a new product to the database (a)
            \r*Make a backup of the entire inventory(b)

            ''')
        choice = input('What would you like to do?: ')
        if choice in ['v', 'a', 'b']:
            return choice
        else:
            input(
                '''
                \rPlease enter one of the options above

                \rletters a, b or v only

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
                print(f'''
                      Product Name: {product.product_name}
                      Product Quantity:{product.product_quantity} units
                      Product Price:${product.product_price/100:.2f}
                      Date last updated:{product.date_updated}
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


def add_product():

    product_name = input('Please enter a product name')
    try:
        product_quantity = int(input('''Please enter the quantityof the product'''))
    except ValueError:
        print('Please enter only whole numbers')
        product_quantity = int(
            input('Please enter the quantity of the product'))
    try:
        product_price = input('Please enter the price for the product')
        transformed_price = clean_price(product_price)
        if type(transformed_price) != int:
            raise Exception('Please enter a valid value for the  price ')
    except Exception as e:
        print(e)
        product_price = input('Please enter the price for the product')
        transformed_price = clean_price(product_price)

    product_in_db = session.query(Product).\
        filter(Product.product_name == product_name).\
        one_or_none()
    # if the product doesn't exist in the database
    if product_in_db is None:
        product_added = Product(product_name=product_name,
                                product_quantity=product_quantity,
                                product_price=transformed_price)
        session.add(product_added)
        session.commit()
    elif product_in_db is not None:
        print('Product already in the system, updating with new details')
        product_in_db.product_price = clean_price(product_price)
        product_in_db.product_quantity = clean_quantity(product_quantity)
        product_in_db.date_updated = datetime.datetime.now()
        session.commit()


def create_backup():
    "creates 2 backup files"

    with open('backup1.csv', 'w') as backup_csv1:
        field_names1 = [
            'product_id',
            'product_name',
            'product_quantity',
            'product_price',
            'date_updated'
            ]

        backup_writer = csv.DictWriter(backup_csv1, fieldnames=field_names1)
        backup_writer.writeheader()
        data = session.query(Product).all()
        for datum in data:
            backup_writer.writerow(
                {
                    'product_id': datum.product_id,
                    'product_name': datum.product_name,
                    'product_quantity': datum.product_quantity,
                    'product_price': datum.product_price,
                    'date_updated': datum.date_updated
                }
                )
    with open('backup2.csv', 'w') as backup_csv2:
        field_names2 = [
            'Product Id',
            'Product Name',
            'Product Quantity',
            'Product Price',
            'Date Updated',
            ]
        backup_writer = csv.DictWriter(backup_csv2, fieldnames=field_names2)
        backup_writer.writeheader()
        data = session.query(Product).all()
        for datum in data:
            backup_writer.writerow(
                {
                    'Product Id': datum.product_id,
                    'Product Name': datum.product_name,
                    'Product Quantity': datum.product_quantity,
                    'Product Price': datum.product_price,
                    'Date Updated': datum.date_updated
                }
                )
    print('backup1.csv and backup2.csv were successfully created')
    print()
    print()


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


def add_csv():

    with open('inventory.csv') as inventory_csv:

        data = csv.DictReader(inventory_csv)

        for row in data:

            product_in_db = session.query(Product).\
                filter(Product.product_name == row['product_name']).\
                one_or_none()

            if product_in_db is None:
                product_name = row['product_name']
                product_price = clean_price(row['product_price'])
                product_quantity = clean_quantity(row['product_quantity'])
                date_updated = clean_date(row['date_updated'])
                new_product = Product(product_name=product_name,
                                      product_quantity=product_quantity,
                                      product_price=product_price,
                                      date_updated=date_updated
                                      )
                session.add(new_product)
            session.commit()
            if product_in_db is not None:

                if product_in_db.product_name == row['product_name']:

                    date_in_db = product_in_db.date_updated

                    csv_date = clean_date(row['date_updated'])
                    if date_in_db > csv_date:
                        print(' updating the database')

                    elif date_in_db < csv_date:

                        print('loading new data from source for product:',
                              product_in_db.product_name)

                        product_in_db.product_price = clean_price(row['product_price'])
                        product_in_db.product_quantity = clean_quantity(row['product_quantity'])
                        product_in_db.date_updated = clean_date(row['date_updated'])

                        session.commit()
                        print('the following changes have been made:')
                        print(product_in_db.product_price)

    print('database is up-to-date')


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
            # add a product
            add_product()

        elif choice == 'b':
            # create backup
            create_backup()
            pass
        else:
            app_running = False
            input(
                '''
                \rPlease enter one of the options above
                \rletters a, b or v only
                \rPress enter to try again: ''')
        print('Thank you for using our system, good bye ')
        sys.exit()


if __name__ == '__main__':

    Base.metadata.create_all(engine)
    app()
