#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import create_engine

from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dicc_Header(Base):
    __tablename__ = "dicc"
    id = Column(Integer, primary_key=True)
    tabla_nombre = Column(String)
    descripcion = Column(String)
    idx_longitud = Column(Integer)
    tabla_relaciones = Column(String)
    indices_secundarios = Column(String)
    accion_grabar = Column(String)

class Dicc_Rows(Base):
    __tablename__ = "dicc_rows"
    id = Column(Integer, primary_key=True)
    dicc_id = Column(Integer, ForeignKey('dicc.id'))
    campo = Column(String)
    descripcion = Column(String)
    formato = Column(String)
    relaciones = Column(String)

class Dicc():
    def __init__(self,filePath):
        # Create an engine that stores data in the local directory's
        # sqlalchemy_example.db file.
        self._fileName = os.path.join(filePath,'manage_test.db')
        self._engine = create_engine('sqlite:///'+self._fileName, echo = True)

        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        Base.metadata.create_all(self._engine)

    def getDiccList(self):
        Session = sessionmaker(bind = self._engine)
        session = Session()

        queryResult = session.query(Dicc_Header).all()
        diccList = []
        for row in queryResult:
            diccList.append(row.tabla_nombre)

        session.close()

        return diccList

    def getDiccHeader(self,tabla_nombre):
        Session = sessionmaker(bind = self._engine)
        session = Session()

        queryResult = session.query(Dicc_Header).filter(Dicc_Header.tabla_nombre == tabla_nombre).all()

        session.close()

        if (len(queryResult) != 1):
            raise ValueError('Nombre de tabla no válido o no existe.')

        return queryResult[0]

    def getDiccRows(self, tabla_nombre):
        pass

    def createDicc(self, tabla_nombre):
        pass

    def deleteDicc(self, tabla_nombre):
        pass

    def saveDicc(self, tabla_nombre, diccHeader, diccRows):
        pass

#############################################################
#
#
##############################################################
if __name__ == "__main__":

    diccEngine = Dicc('.')
    diccList = diccEngine.getDiccList()
    print('----- All diccs:')
    print(diccList)

    data = diccEngine.getDiccHeader('clientes')
    print('----- One Dicc:')
    print(data.tabla_nombre,data.descripcion)
