#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx
import OC
import pickle
from OC.Funciones import *

class gastos(OC.Ventana):
    """ Ficha para manejar los gastos """

    def __init__(self,padre=None):
        OC.Ventana.__init__(self, padre,'Gastos',tam=(800,500))
        #
        ls_campos = []

        # TABBOX
        tb = ['TABBOX','TBG',0,0,600,300,'','','',[]]

        # PN1 - Pestaña General
        pn1 = ['PANEL','PN1',0,0,-1,-1,'','','General',[]]
        #cols=[['Ventana','l'],['Descripción','l']]
        #ls = ['LIST','L1',0,0,-1,-1,cols,'','','','','a_sele_win','','']
        #p0[-1].append(ls)
        eng = ['ENTRYS','ENG','25','50','','',[]]
        #eng[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        eng[-1].append(['IDX','Codigo','5','20','6','%','6','','','','a_LEE_RG','','','',''])
        eng[-1].append(['GA_DENO','Descripción','-1','','50','l','100','','','','','','','',''])
        eng[-1].append(['GA_FEC','Fecha','-1','','10','d','10','','','','','','','',''])
        eng[-1].append(['GA_IMPO','Importe','-1','','10','2','10','','','','','','','',''])
        pn1[-1].append(eng)
        tb[-1].append(pn1)


        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',600,200,200,270,'','','',[]]
        btn=[]
        btn.append(['B1',5,10,95,'left.png','Anterior','a_PREV','Registro Anterior',''])
        btn.append(['B2',105,10,95,'right.png','Siguiente','a_NEXT','Registro Posterior',''])
        btn.append(['B3',5,70,95,'new.png','Nuevo','a_NUEVO','Nuevo Registro',''])
        btn.append(['B4',105,70,95,'save.png','Grabar','a_GRABA','Grabar Datos',''])
        btn.append(['B5',5,140,95,'delete.png','Borrar','a_BORRA','Borrar Registro',''])
        btn.append(['B6',105,140,95,'report.png','Listado','a_INFO','',''])
        btn.append(['B7',5,210,95,'select.png','Buscar','a_INFO:gastos,ga_ls,LS','',''])
        btn.append(['B8',105,210,95,'exit.png','Salir','a_SALIR','',''])
        p3[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(tb)
        ls_campos.append(p3)

        #P4 - Lista de Selección
        p4 = ['PANEL','P4',0,300,600,170,'','','',[]]
        cols = [['Codigo','l'],['Descripcion','l'],['Fecha','d'],['Importe','2']]
        ls = ['LIST','LS',0,0,-1,-1,cols,'','','','','','a_carga_rg','']
        p4[-1].append(ls)

        ls_campos.append(p4)
        #
        self.init_ctrls(ls_campos)
        #
        self._idx = 'IDX'
        self._filedb = 'gastos'
        self._accini=''      # Acción al cargar la ventana
        self._accleer = ''   # Acción despues de leer registro
        self._btfin = ''     # Nombre del boton a ejecutar cuando pulse boton FIN


    #
    #-- Acciones a ejecutar
    #
    def Ejecuta_Accion(self,accion,obj=None):

        """ Acciones a ejecutar """
        # Probamos primero si es una accion estandar
        std = OC.Ventana.Ejecuta_Accion(self, accion,obj)
        ok,val = std

        # Comprobar el valor devuelto por si hay que hacer algo
        # Ya se ejecutó la accion. No continuar con la accion normal
        if ok>0:
            return val

        if accion=='a_carga_rg':
            cod=self._ct['LS'].GetValue()
            if cod<>None: self._ct[self._idx].SetValue(cod)

        return 0


#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App(False)
    ventana = gastos()
    ventana.Show()
    app.MainLoop()

