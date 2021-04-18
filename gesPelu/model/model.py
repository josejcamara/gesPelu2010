# https://realpython.com/python-sqlite-sqlalchemy/
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_declaring_mapping.htm

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from sqlalchemy import create_engine
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db', echo = True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Customer(Base):
    __tablename__ = "clientes"
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    postal = Column(String)
    city = Column(String)
    phone = Column(String)
    email = Column(String)

class Invoice(Base):
   __tablename__ = 'invoices'
   
   id = Column(Integer, primary_key = True)
   custid = Column(Integer, ForeignKey('clientes.customer_id'))
   invno = Column(Integer)
   amount = Column(Integer)
   customer = relationship("Customer", back_populates = "invoices")

#
#
#
Customer.invoices = relationship("Invoice", order_by = Invoice.id, back_populates = "customer")

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

# Insert
result = session.query(Customer).filter(Customer.email == 'ravi@gmail.com')
if (result.scalar()) > 0:
    print "Ravi already exists"
    c1 = result[0]
else:
    c1 = Customer(first_name = 'Ravi Kumar', address = 'Station Road Nanded', email = 'ravi@gmail.com')
    session.add(c1)
    session.commit()

# c1.invoices = [Invoice(invno = 10, amount = 15000), Invoice(invno = 14, amount = 3850)]
# session.commit()

# Query
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_filter_operators.htm
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_common_relationship_operators.htm
session.query(Customer).filter(Customer.customer_id == 2).update({Customer.first_name:"Mr."+Customer.first_name}, synchronize_session = False)
session.commit()

result = session.query(Customer).all()

for row in result:
   print ("Name: ",row.first_name, "Address:",row.address, "Email:",row.email)

for c, i in session.query(Customer, Invoice).filter(Customer.customer_id == Invoice.custid).all():
   print ("ID: {} Name: {} Invoice No: {} Amount: {}".format(c.customer_id,c.first_name, i.invno, i.amount))

print('-------------------------------')

result = session.query(Customer).join(Invoice).filter(Invoice.amount == 15000).all()
for row in result:
   for inv in row.invoices:
      print (row.customer_id, row.first_name, inv.invno, inv.amount)