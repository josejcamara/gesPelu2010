# https://realpython.com/python-sqlite-sqlalchemy/

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()

# client_publisher = Table(
#     "client_publisher",
#     Base.metadata,
#     Column("client_id", Integer, ForeignKey("client.client_id")),
#     Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
# )

class Customer(Base):
    __tablename__ = "clientes"
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    postal = Column(String)
    city = Column(String)
    phone = Column(String)
    # books = relationship("Book", backref=backref("author"))
    # publishers = relationship(
    #     "Publisher", secondary=client_publisher, back_populates="authors"
    # )

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)