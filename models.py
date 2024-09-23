import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker,relationship



# Initialize Sqlite database
engine = create_engine('sqlite:///inventory.db', echo=False)
# on sqlachemy 2.0 declarative_base has been replaced by Declarative Base
# create the Declarative Base

# this is the new form as per sqlalchemy 2.0


class Base(DeclarativeBase):
    pass


Session = sessionmaker(engine)
session = Session()


# Create your database model called Product
class Product(Base):

    __tablename__ = 'products'

    # Attributes
    # Product_id=Primary_key,
    # product_name,
    # product_quantity,
    # product_price,
    # date_updated.
    #brand id (ForeignKey)
    product_id = Column('Product Id', Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Product Quantity', Integer)
    product_price = Column('Product Price', Integer)
    date_updated = Column('Date Updated', Date, default=datetime.datetime.now)
    brand_id=Column('brand_id', ForeignKey("Brands.Brand Id"))

    
    def __repr__(self) -> str:
        ...
        return f"'Product Name:{self.product_name},\
            Quantity: {self.product_quantity}, \
            Price: {self.product_price}, \
            Date Updated: {self.date_updated} "

class Brand(Base):
    __tablename__='Brands'
    brand_id = Column('Brand Id', Integer, primary_key=True)
    
    brand_name = Column('Brand Name', String)
    product=relationship("Product")


    def __repr__(self)->str:
        pass
    

        