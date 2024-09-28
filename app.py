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



#loading function
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

#menu
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
    try:
        product_quantity = int(
            input('''Please enter the quantity of the product'''))
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
    brand_name=input('Please enter a brand name')
    

    product_in_db = session.query(Product).\
        filter(Product.product_name == product_name).\
        one_or_none()
    # if the product doesn't exist in the database
    if product_in_db is None:
        brand_in_db = session.query(Brand).\
            filter(Brand.brand_name == brand_name).\
            one_or_none()
        if brand_in_db is None:
            new_brand=Brand(brand_name=brand_name)
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
        product_in_db.brand_id=product_in_db.brand_id

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
    while app_running:
        choice = menu()

        if choice == 'v':
            # view a single product
            view_product()
        elif choice == 'a':
            pass

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