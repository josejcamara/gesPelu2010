#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import create_engine

from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from sqlalchemy.types import TypeDecorator, Unicode


Base = declarative_base()

class CoerceUTF8(TypeDecorator):
    """
        Safely coerce Python bytestrings to Unicode
        before passing off to the database.
        https://docs.sqlalchemy.org/en/14/core/custom_types.html#coercing-encoded-strings-to-unicode
    """

    impl = Unicode

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            value = value.decode('utf-8')
        return value


class Form(Base):
    __tablename__ = "form"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(CoerceUTF8)
    accion_antes = Column(String)
    accion_rellena = Column(String)
    accion_despues = Column(String)
    rows = relationship("Form_Rows", cascade="all, delete")

    def __str__(self):
        outputLines = [] 
        outputLines.append("Form(%d): %s" % (self.id, self.nombre))
        for row in self.rows:
            outputLines.append(str(row))

        return '\n'.join(outputLines)

class Form_Rows(Base):
    __tablename__ = "form_rows"
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey('form.id'))
    campo = Column(String)
    titulo = Column(CoerceUTF8)
    formato = Column(String)
    longitud = Column(Integer)
    formula_calculo = Column(String)

    def __str__(self):
        return("_Row(%d): Form(%s), %s, %s" % (self.id, self.form_id, self.campo, self.formato))

#############################################################
#
#
##############################################################
def prepareEngine(filePath, fileName='forms.db', enableEcho = False):
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    _fileName = os.path.join(filePath,fileName)
    _engine = create_engine('sqlite:///'+_fileName, echo = enableEcho)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(_engine)

    return _engine

if __name__ == "__main__":

    engine = prepareEngine('.')
    #
    Session = sessionmaker(bind = engine)
    session = Session()
    #
    form1 = Form(nombre='ar_ls1', descripcion=u'Lista de Artículos')
    form1_row1 = Form_Rows(campo='IDX', titulo=u'Código', formato='l')
    form1_row2 = Form_Rows(campo='AR_DENO', titulo=u'Nombre Artículo', formato='l')
    form1.rows = [form1_row1, form1_row2]
    session.add(form1)
    session.commit()
    #

    search = session.query(Form).filter(Form.nombre == 'ar_ls1').first()
    # if search == None:
    print(search)
    # print(search.rows)


    session.close()
