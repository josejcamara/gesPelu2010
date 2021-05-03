#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import create_engine

from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from sqlalchemy.types import TypeDecorator, Unicode

from sqlalchemy.ext.declarative import declarative_base

class CoerceUTF8(TypeDecorator):
    """Safely coerce Python bytestrings to Unicode
    before passing off to the database."""

    impl = Unicode

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            value = value.decode('latin-1')
        return value

Base = declarative_base()

class Dicc_Header(Base):
    __tablename__ = "dicc"
    id = Column(Integer, primary_key=True)
    tabla_nombre = Column(String)
    descripcion = Column(CoerceUTF8)
    idx_longitud = Column(Integer)
    tabla_relaciones = Column(String)
    indices_secundarios = Column(String)
    accion_grabar = Column(String)

    def __str__(self):
        return("Dicc_Header(%d): %s, %s, %s" % (self.id, self.tabla_nombre, self.descripcion, self.accion_grabar))

class Dicc_Rows(Base):
    __tablename__ = "dicc_rows"
    id = Column(Integer, primary_key=True)
    dicc_id = Column(Integer, ForeignKey('dicc.id'))
    campo = Column(String)
    descripcion = Column(CoerceUTF8)
    formato = Column(String)
    tabla_relacion = Column(String)
    formula_calculo = Column(String)

    def __str__(self):
        return("Dicc_Row(%d): %s, %s, %s" % (self.id, self.dicc_id, self.campo, self.formato))

class Dicc():
    def __init__(self, filePath, fileName='dicc.db', ui=None, enableEcho = False):
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

    def getDiccList(self):
        Session = sessionmaker(bind = self._engine)
        session = Session()

        queryResult = session.query(Dicc_Header).all()
        diccList = []
        for row in queryResult:
            diccList.append([row.tabla_nombre, row.descripcion])

        session.close()

        return diccList

    def getDicc(self, tabla_nombre):
        datos = self.getDiccHeader(tabla_nombre)
        datos.append(self.getDiccRows(tabla_nombre))
        return datos

    def getDiccHeader(self,tabla_nombre):
        Session = sessionmaker(bind = self._engine)
        session = Session()

        queryResult = session.query(Dicc_Header).filter(Dicc_Header.tabla_nombre == tabla_nombre).all()

        session.close()

        if (len(queryResult) != 1):
            #raise ValueError('Nombre de tabla no válido o no existe.')
            self.alert("Nombre de tabla %s no válido o no existe" % tabla_nombre)
            return []

        header = queryResult[0]
        data = []
        # data.append(header.tabla_nombre)
        data.append(header.descripcion)
        data.append(header.idx_longitud)
        data.append(header.tabla_relaciones)
        data.append(header.indices_secundarios)
        data.append(header.accion_grabar)

        return data

    def getDiccRows(self, tabla_nombre):
        Session = sessionmaker(bind = self._engine)
        session = Session()

        data = []
        for h, r in session.query(Dicc_Header, Dicc_Rows).filter(Dicc_Header.tabla_nombre == tabla_nombre).all():
            if (r.dicc_id != h.id): continue
            data.append([r.campo, r.descripcion, r.formato, r.tabla_relacion, r.formula_calculo])

        session.close()

        return data

    def createDicc(self, tabla_nombre):
        Session = sessionmaker(bind = self._engine)
        session = Session()

        queryResult = session.query(Dicc_Header).filter(Dicc_Header.tabla_nombre == tabla_nombre).all()
        if len(queryResult) > 0:
            self.alert("No se puede crear '%s', ya existe" % tabla_nombre)
            return -1
        else:
            c1 = Dicc_Header(tabla_nombre = tabla_nombre, descripcion = '')
            session.add(c1)
            session.commit()
        session.close()

        return 0

    def deleteDicc(self, tabla_nombre):
        Session = sessionmaker(bind = self._engine)
        session = Session()

        queryResult = session.query(Dicc_Header).filter(Dicc_Header.tabla_nombre == tabla_nombre).delete(synchronize_session=False)

        session.commit()
        session.close()

        return (0 if queryResult == 1 else -1)

    def updateDicc(self, tabla_nombre, diccHeaderData, diccRowsData):
        Session = sessionmaker(bind = self._engine)
        session = Session()

        diccHeader = session.query(Dicc_Header).filter(Dicc_Header.tabla_nombre == tabla_nombre).first()
        if diccHeader == None:
            # self.alert("No se puede actualizar '%s', no existe" % tabla_nombre)
            # return -1
            self.createDicc(tabla_nombre)
            diccHeader = session.query(Dicc_Header).filter(Dicc_Header.tabla_nombre == tabla_nombre).first()

        dicc_id = diccHeader.id
        session.query(Dicc_Rows).filter(Dicc_Rows.dicc_id == dicc_id).delete(synchronize_session=False)

        diccHeader.descripcion = diccHeaderData[0]
        diccHeader.idx_longitud = diccHeaderData[1]
        diccHeader.tabla_relaciones = diccHeaderData[2]
        diccHeader.indices_secundarios = diccHeaderData[3]
        diccHeader.accion_grabar = diccHeaderData[4]

        for lnRow in diccRowsData:
            row = Dicc_Rows()
            row.dicc_id = dicc_id
            row.campo = lnRow[0]
            row.descripcion = lnRow[1]
            row.formato = lnRow[2]
            row.tabla_relacion = lnRow[3]
            row.formula_calculo = lnRow[4]
            session.add(row)

        
        session.commit()
        session.close()

        return 0

#############################################################
#
#
##############################################################
if __name__ == "__main__":

    diccEngine = Dicc('.','dicc.test.db')
    #
    diccEngine.createDicc('prueba')

    print('----- All diccs:')
    diccList = diccEngine.getDiccList()
    print(diccList)

    diccEngine.deleteDicc('prueba')

    print('----- All diccs:')
    diccList = diccEngine.getDiccList()
    print(diccList)
    exit(1)


    data = diccEngine.getDiccHeader('clientes')
    print('----- One Dicc:')
    print(data.tabla_nombre,data.descripcion)

    data = diccEngine.getDiccRows('clientes')
    print('----- One Dicc Rows:')
    for r in data:
        print(r.campo, r.descripcion)
