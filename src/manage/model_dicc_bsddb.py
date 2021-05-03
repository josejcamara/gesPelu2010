#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import bsddb
import pickle


class Dicc():
    def __init__(self, filePath, fileName='dicc', ui=None, enableEcho = False):
        # Create an engine that stores data in the local directory's
        # sqlalchemy_example.db file.
        self._ui = ui
        self._fileName = os.path.join(filePath,fileName)

    def alert(self, message):
        if (self._ui != None):
            # TODO: wx message
            pass
        else:
            print(message)
            # raise ValueError(message)  ### raise or print??

    def getDiccList(self):
        diccList=[]
        dicc = bsddb.btopen(self._fileName)
        for dc in dicc.keys():
            datos = pickle.loads(dicc[dc])
            diccList.append([dc,datos[0]]) # Archivo, Descripcion
        dicc.close()

        return diccList

    def getDicc(self, tabla_nombre):
        datos = self.getDiccHeader(tabla_nombre)
        datos.append(self.getDiccRows(tabla_nombre))
        return datos

    def getDiccHeader(self,tabla_nombre):
        dicc = bsddb.btopen(self._fileName)
        if (not tabla_nombre in dicc):
            dicc.close()
            return []
        datos = pickle.loads(dicc[tabla_nombre])
        dicc.close()
        return datos[:-1]

    def getDiccRows(self, tabla_nombre):
        dicc = bsddb.btopen(self._fileName)
        if (not tabla_nombre in dicc):
            dicc.close()
            return []
        datos = pickle.loads(dicc[tabla_nombre])
        dicc.close()

        res = []
        for ln in datos[-1]:
            if ln[0]=='': continue
            res.append(ln)

        return res

    def createDicc(self, tabla_nombre):
        dicc = bsddb.btopen(self._fileName)
        if (tabla_nombre in dicc):
            dicc.close()
            return -1
        dicc.close()

        self.updateDicc(tabla_nombre,['','','',''],[])
        return 0

    def deleteDicc(self, tabla_nombre):
        dicc = bsddb.btopen(self._fileName)
        if (not tabla_nombre in dicc):
            dicc.close()
            return -1
        del dicc[tabla_nombre]
        dicc.close()
        return 0

    def updateDicc(self, tabla_nombre, diccHeader, diccRows):
        datos = diccHeader
        datos.append(diccRows)
        dicc = bsddb.btopen(self._fileName)
        dicc[tabla_nombre]=pickle.dumps(datos)
        dicc.close()
        return 0

#############################################################
#
#
##############################################################
if __name__ == "__main__":

    diccEngine = Dicc('.')
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
