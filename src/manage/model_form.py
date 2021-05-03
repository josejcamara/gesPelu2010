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
    tabla = Column(String)
    nombre = Column(String)
    descripcion = Column(CoerceUTF8)
    accion_antes = Column(String)
    accion_rellena = Column(String)
    accion_despues = Column(String)
    rows = relationship("Form_Rows", cascade="all, delete")
    filters = relationship("Form_Filters", cascade="all, delete")

    def __str__(self):
        outputLines = [] 
        outputLines.append("Form(%d): %s" % (self.id, self.nombre))
        for row in self.rows:
            outputLines.append(str(row))
        for filter in self.filters:
            outputLines.append(str(filter))

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

class Form_Filters(Base):
    __tablename__ = "form_filters"
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey('form.id'))
    campo = Column(String)
    titulo = Column(CoerceUTF8)
    formato = Column(String)
    longitud = Column(Integer)
    operation = Column(String)

    def __str__(self):
        return("_Filter(%d): Form(%s), %s, %s" % (self.id, self.form_id, self.campo, self.operation))

class FormsManager():

    def __init__(self, filePath, fileName='forms.db', ui=None, enableEcho = False):
        # Create an engine that stores data in the local directory's
        # sqlalchemy_example.db file.
        self._ui = ui
        self._fileName = os.path.join(filePath,fileName)
        self._engine = create_engine('sqlite:///'+self._fileName, echo = enableEcho)

        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        Base.metadata.create_all(self._engine)

    def alert(self, message):
        if (self._ui != None):
            # TODO: wx message
            pass
        else:
            print(message)
            # raise ValueError(message)  ### raise or print??

    def getTablesWithForm(self):
        Session = sessionmaker(bind = self._engine)
        session = Session()   

        tablesSet = set()
        formList = session.query(Form).filter().all()
        for form in formList:
            tablesSet.add(form.tabla)

        session.close()

        return list(tablesSet)

    def getFormsForTable(self, nombreTabla):
        Session = sessionmaker(bind = self._engine)
        session = Session()   

        formList = session.query(Form).filter(Form.tabla == nombreTabla).all()
        if len(formList) == 0:
            self.alert(u"No hay informes para la tabla '%s'." % nombreTabla)
            return []

        formsResultMap = {}
        for form in formList:
            formData = []
            formData.append(form.descripcion)
            formData.append(form.accion_antes)
            formData.append(form.accion_rellena)
            formData.append(form.accion_despues)
            rows = []
            for row in form.rows:
                rows.append([row.campo, row.titulo, row.formato, row.longitud, row.formula_calculo])
            formData.append(rows)
            filters = []
            for filter in form.filters:
                filters.append([filter.campo, filter.titulo, filter.formato, filter.longitud, filter.operation])
            formData.append(filters)
            #
            formsResultMap[form.nombre] = formData

        session.commit()
        session.close()

        return formsResultMap

#############################################################
#
#
##############################################################
if __name__ == "__main__":
    # # ----
    # _engine = create_engine('sqlite:///forms.test.db', echo = True)
    # Base.metadata.create_all(_engine)
    # #
    # Session = sessionmaker(bind = _engine)
    # session = Session()
    # #
    # form1 = Form(tabla='clientes', nombre='cl_ls1', descripcion=u'Lista de Clientes')
    # form1_row1 = Form_Rows(campo='IDX', titulo=u'Código', formato='l')
    # form1_row2 = Form_Rows(campo='CL_DENO', titulo=u'Nombre Cliente', formato='l')
    # form1.rows = [form1_row1, form1_row2]
    # form1_filter1 = Form_Filters(campo='CL_DENO', operation='=')
    # form1.filters = [form1_filter1]
    # session.add(form1)
    # session.commit()
    # session.close()
    # # ----

    formManager = FormsManager('.','forms.test.db')
    tablas = formManager.getTablesWithForm()
    print(tablas)

    data = formManager.getFormsForTable('clientes')
    print(data)

