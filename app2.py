'''Store Inventory App

This script allows the user to:

-Initializes a Sqlite database
-Creates a database model called Product
-Creates a database model called Brand
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
from models import Base, session, Product, Brand, engine


def menu():
    '''
    Menu
    creates a menu for the application
    args:None
    Returns:str

    '''
   


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








def app():
    try:
        add_csv()
    except (FileNotFoundError):
        print()
        print()
        print('No source csv found, please review')
        print()
        print()
    """
    app_running = True
    while app_running:
        choice = menu()

        if choice == 'v':
            # view a single product
            view_product()
        elif choice == 'a':
            pass
            
            #analyze()

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
                \rPress enter to try again: ''')
        print('Thank you for using our system, good bye ')
    """
    # sys.exit()


if __name__ == '__main__':

    Base.metadata.create_all(engine)
    app()
