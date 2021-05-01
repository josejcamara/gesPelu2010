#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx, os
import OC
import bsddb
import pickle
from OC.Funciones import *

class Manage_Dicc(OC.Ventana):
    """ Ficha para manejar los archivos de la base de datos """

    def __init__(self,filePath):
        #
        self.filePath = filePath
        self.fileName = os.path.join(filePath,'dicc')
        #
        OC.Ventana.__init__(self, None,'Tablas de la Aplicación',tam=(800,600))
        #
        ls_campos = []
        #
        p1 = ['PANEL','P1',0,150,200,420,'','','',[]]
        #---
        hp1=[]  # hijos de P1
        cols=[['Nombre','l'],['Descripción','l']]
        ls1 = ['LIST','L1',0,0,-1,-1,cols,'','','','','a_pon_dic','a_sele_dicc','']
        hp1.append(ls1)
        p1[-1]=hp1
        #

        # p2 ==> Imagen del logo...???
        p2 = ['PANEL','P2',200,0,600,250,'','','',[]]
        hp2=[]
        lse = []    # Entradas
        lse.append(['DENO','Nombre Tabla',10,20,10,'l',0,'','','','','','','',''])
        lse.append(['DESC','Descripción',-1,0,40,'l',0,'','','','','','','',''])
        lse.append(['LCOD','Long. Fija',-1,0,5,'i',0,'','','','','','','',''])
        lse.append(['RELS','Tablas Relacionadas',10,-1,30,'l',0,'','','','','','Nombre de las tablas relacionadas, separadas por comas','',''])
        lse.append(['INDICES','Indices Secundarios',-1,0,26,'l',0,'','','','','','Código Postal','',''])
        lse.append(['ACCGRAB','Acción al Grabar',10,-1,25,'l',0,'','','','','','','',''])
        hp2.append(['ENTRYS','EX',25,50,'','',lse])
        #
        btn=[]
        btn.append(['B1',10,200,90,'new.png','Nuevo','a_nuevo','Crear una nueva tabla',''])
        btn.append(['B2',110,200,90,'save.png','Grabar','a_graba','Grabar cambios en la tabla',''])
        btn.append(['B3',210,200,90,'delete.png','Borrar','a_borra','',''])
        btn.append(['B9',510,200,90,'exit.png','Salir','a_salir','',''])
        #
        hp2.append(['BUTTONS','BTX',50,'','',btn])

        #---
        p2[-1] = hp2
        #---

        p3 = ['PANEL','P3',200,250,600,320,'','','',[]]
        #---
        cols = []
        cols.append(['Campo',7,'l',0,'','','','','','','','','',''])
        cols.append(['Descripción',22,'l',0,'','','','','','','','','',''])
        cols.append(['Formatos',10,'l',0,'','','','','','','','','',''])
        cols.append(['Relaciones',15,'l',0,'','','','','','','','','',''])
        cols.append(['F.Calculo',20,'l',0,'','','','','','','','','',''])
        #
        p3[-1].append(['GRID','G1','',2,22,590,22,11,cols,2,'',''])
        #---

        #
        ls_campos.append(p1)
        ls_campos.append(p2)
        ls_campos.append(p3)
        #
        self.init_ctrls(ls_campos)
        #
        self.Ejecuta_Accion('a_carga_dicc')

    def Ejecuta_Accion(self,accion):
        """ Acciones a ejecutar """

        if accion=='a_salir':
            self.Close()
            self.Destroy()
        elif accion=='a_nuevo':
            self._ct['DENO'].SetValue('')
            self._ct['DESC'].SetValue('')
            self._ct['LCOD'].SetValue('')
            self._ct['RELS'].SetValue('')
            self._ct['INDICES'].SetValue('')
            self._ct['ACCGRAB'].SetValue('')
            self._ct['G1'].SetValue([])
        elif accion=='a_carga_dicc':
            """ Leer la lista de tablas actuales """
            lis=[]
            dicc = bsddb.btopen(self.fileName)
            for dc in dicc.keys():
                datos = pickle.loads(dicc[dc])
                lis.append([dc,datos[0]]) # Archivo, Descripcion
            dicc.close()
            self._ct['L1'].SetValue(lis)
        elif accion=='a_pon_dic':
            """ Pone los datos del diccionario selecionado"""
            if self.Modifica==1:
                dlg = Men('Ha modificado los datos.¿Desea Continuar sin grabar?','sn',img='q')
                if dlg=='n': return -1
            tabla = self._ct['L1'].GetValue()
            dicc = bsddb.btopen(self.fileName)
            datos = pickle.loads(dicc[tabla])
            dicc.close()
            self._ct['DENO'].SetValue(tabla)
            self._ct['DESC'].SetValue(datos[0])
            self._ct['LCOD'].SetValue(datos[1])
            self._ct['RELS'].SetValue(datos[2])
            self._ct['INDICES'].SetValue(datos[3])
            self._ct['ACCGRAB'].SetValue(datos[4])
            self._ct['G1'].SetValue(datos[-1])
            self.Modifica=0

        elif accion=='a_borra':
            """ Borrar una tabla """
            sele = self._ct['L1'].GetValue()
            if sele=='':
                Men('Debe seleccionar el fichero a borrar')
                return -1
            dlg = Men('¿Está seguro de borrar la tabla '+sele+'?','sn',img='q')
            if dlg=='n': return -1
            dicc = bsddb.btopen(self.fileName)
            del dicc[sele]
            dicc.close()
            Men('Tabla Borrada')
            self.Ejecuta_Accion('a_carga_dicc')

        elif accion=='a_graba':
            """ Grabar los datos de la tabla actual """
            tabla = self._ct['DENO'].GetValue().lower()
            desc = self._ct['DESC'].GetValue()
            lcod = self._ct['LCOD'].GetValue()
            rels = self._ct['RELS'].GetValue()
            indx = self._ct['INDICES'].GetValue()
            accg = self._ct['ACCGRAB'].GetValue()
            campos = self._ct['G1'].GetValue()

            if tabla=='':
                Men('No hay nombre de tabla a grabar.')
                return -1    # No ha indicado nada que grabar
            if campos==[]:
                Men('No ha indicado los campos del diccionario')
                return -1
            # datos del fichero => "dicc". dicc[tabla] = ...
            # 0 - Descripción de la tabla
            # 1 - Longitud del codigo (Si fija)
            # 2 - Tablas Relacionadas
            # 3 - Indices Secundarios
            # 4 - Accion de grabación
            # 5 - Lista de Campos
            datos = [desc,lcod,rels,indx,accg,campos]

            #
            dicc = bsddb.btopen(self.fileName)
            dicc[tabla]=pickle.dumps(datos)
            dicc.close()
            #
            Men('Registro Guardado',img='i')
            self.Ejecuta_Accion('a_carga_dicc')



#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App(False)
    ventana = Manage_Dicc()
    #ventana._init_ctrls(ls_campos)
    ventana.Show()
    app.MainLoop()
