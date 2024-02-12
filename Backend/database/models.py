from datetime import date, timedelta #import 
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func 

#Declare on the MAIN  DATA-BASE that all data will sync to ---Base = declarative_base()---
Base = declarative_base()
# איך שבנוי הדאטה בייס , כל הקבצים נמצאים כאן וזה נועד כדי לבנות את כל הטבלאות ואת המשתמשים בעצמו


  #Represent the 'book' table on the DATA-BASE
class Books(Base):
    __tablename__ = 'books' #name of the table in DATA-BASE
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year_published = Column(Integer)
    book_type = Column(Integer) # One: up to 10 days, Two: up to 5 days, Three: up to 2 days
    removed = Column(Boolean)
    loans = relationship('Loans', back_populates='book')#connect between the tables 'loans' and 'books' in DATA-BASE 

#Represent the 'customers' table on the DATA-BASE
class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    city = Column(String)
    age = Column(Integer)
    removed = Column(Boolean)
    loans = relationship('Loans', back_populates='customer') #connect between the tables 'loans' and 'customer' 
    #---- in DATA-BASE 

#Represent the 'loans' table on the DATA-BASE
class Loans(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    loan_date = Column(Date)
    return_date = Column(Date)
    customer = relationship('Customers', back_populates='loans')
    book = relationship('Books', back_populates='loans')

#check what if the client late of return book on-time and limit the loan time
    def is_late(self):
        if self.loan_date is not None:
            # Calculate the difference between the return_date and today's date
            days_difference = (date.today() - self.loan_date).days

            # Check if the difference exceeds the allowed days based on book_type
            if self.book.book_type == 1 and days_difference > 10:
                return True
            elif self.book.book_type == 2 and days_difference > 5:
                return True
            elif self.book.book_type == 3 and days_difference > 2:
                return True

        return False   #IF THE CUSTOMER NOT PICK LOAN TIME RETURN *FALSE* and stop the function from work

engine = create_engine('sqlite:///db.sqlite3')
Base.metadata.create_all(bind=engine)