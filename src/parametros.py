#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
#from OC import Ventana
import OC
from OC.Funciones import *

class parametros(OC.Ventana):
    """ Ficha de parametros de configuración """

    def __init__(self):
        OC.Ventana.__init__(self, None,'Configuración de la Aplicación',tam=(800,600))
        #
        self._idx = 'IDX'
        self._filedb = 'parametros'
        self._accini = 'a_ini_var'
        #
        ls_campos = []
        #
        p1 = ['PANEL','P1',0,0,600,-1,'','','',[]]
        #---
        hp1=[]  # hijos de P1
        #
        lse = []    # Entradas
        lse.append(['IDX','Cod',10,20,4,'l',1,'n','','','a_LEE_RG','','','',''])
        lse.append(['P_DENO','Nombre Empresa',-1,0,40,'l',40,'','','','','','','',''])
        lse.append(['P_CIF','NIF',-1,0,10,'l',10,'','','','','','','',''])
        lse.append(['P_NOM','Razon Social',10,-1,20,'l',30,'','','','','','Nombre Fiscal','',''])
        lse.append(['P_DIR','Direccion',-1,0,40,'l',25,'','','','','','','',''])
        lse.append(['P_POB','Población',10,-1,40,'l',25,'','','','','','','',''])
        lse.append(['P_CP','C.Postal',-1,0,10,'l',5,'','','','','','Código Postal','',''])
        lse.append(['P_PROV','Provincia',-1,0,20,'l',0,'','','','','','','',''])
        lse.append(['P_EJA','Ejercicio Actual',10,-1,10,'l',10,'','','','','','','',''])
        lse.append(['P_FINI','Inicio Ejercicio',-1,0,10,'d',10,'','','','','','','',''])
        lse.append(['P_FFIN','Fin Ejercicio',-1,0,10,'d',10,'','','','','','','',''])
        lse.append(['P_LOGO','Logo Empresa',10,-1,30,'l',30,'','','','','','','',''])
        #
        hp1.append(['ENTRYS','E1',25,50,'','',lse])
        #---
        p1[-1] = hp1

        # p2 ==> Imagen del logo...???
        p2 = ['PANEL','P2',600,0,200,150,'B-36:244:26/RF',[]]
        #---

        p3 = ['PANEL','P3',600,150,200,420,'',[]]
        #---
        hp3=[]
        btn=[]
        #btn.append(['B1',10,10,80,'back.gif','Anterior','a_PREV','Registro Anterior'])
        #btn.append(['B2',100,10,80,'next.gif','Proximo','a_NEXT','Registro Siguiente'])
        btn.append(['B4',100,70,95,'save.png','Grabar','a_GRABA','Grabar Registro'])
        btn.append(['B6',10,350,95,'undo.png','Salir','a_SALIR','Salir de la ventana'])
        #
        hp3.append(['BUTTONS','BTN',50,'','',btn])
        #
        p3[-1] = hp3
        #
        ls_campos.append(p1)
        ls_campos.append(p2)
        ls_campos.append(p3)
        #
        self.init_ctrls(ls_campos)
        #
        if self._accini<>'':
            self.Ejecuta_Accion(self._accini)

    def Ejecuta_Accion(self,accion,obj=None):
        """ Acciones a ejecutar """
        # Probamos primero si es una accion estandar
        std = OC.Ventana.Ejecuta_Accion(self, accion, obj)
        ok,val = std

        # Comprobar el valor devuelto por si hay que hacer algo
        # Ya se ejecutó la accion. No continuar con la accion normal
        if ok>0:
            return val

        print 'Ejecutando Accion Propia Parametros: '+accion
        if accion=='a_ini_var':
            self._ct['IDX'].SetValue('0')
            #rg = lee('parametros','0')
            #if rg==1:
            #    Men('No se pudo leer la ficha de parametros')
            #    return
            #else:
            #    pass

#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.PySimpleApp()
    ventana = parametros()
    #ventana._init_ctrls(ls_campos)
    ventana.Show()
    app.MainLoop()