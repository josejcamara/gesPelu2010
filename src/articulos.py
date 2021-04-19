#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import OC
import pickle
from OC.Funciones import *

class articulos(OC.Ventana):
    """ Ficha para manejar las ventanas de la aplicaci�n """

    def __init__(self,padre=None):
        OC.Ventana.__init__(self, padre,'Articulos',tam=(800,600))
        #
        ls_campos = []

        # TABBOX
        tb = ['TABBOX','TBG',0,0,600,400,'','','a_cambia_tab',[]]

        # PN1 - Pesta�a General
        pn1 = ['PANEL','PN1',0,0,-1,-1,'','','General',[]]
        #cols=[['Ventana','l'],['Descripci�n','l']]
        #ls = ['LIST','L1',0,0,-1,-1,cols,'','','','','a_sele_win','','']
        #p0[-1].append(ls)
        eng = ['ENTRYS','ENG','25','50','','',[]]
        #eng[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        eng[-1].append(['IDX','Codigo','5','20','6','%','6','','','','a_LEE_RG','','','',''])
        eng[-1].append(['AR_DENO','Nombre Art�culo','-1','','50','l','100','','','','','','','',''])
        eng[-1].append(['AR_CBAR','C�digo Barras','-1','','15','l','100','','','','','','','',''])
        eng[-1].append(['AR_TIPO','Tipo','-1','','5','l','5','','','','','LISTA:A-Articulo|S-Servicio]1','','',''])
        eng[-1].append(['AR_PVP','PVP','-1','','6','2','10','','','','','','','',''])
        eng[-1].append(['AR_STK','Stock','-1','','6','0','10','','','','','','','',''])
        pn1[-1].append(eng)
        tb[-1].append(pn1)

        """# PN2 - Historico Ventas
        pn3 = ['PANEL','PN2',200,0,600,500,'','','Historico Ventas',[]]
        cols=[['Codigo','%'],['Fecha','d'],['Importe','2']]
        ls = ['LIST','L1',10,10,580,340,cols,'','','','','','','']
        pn3[-1].append(ls)
        tb[-1].append(pn3)"""


        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',600,200,200,370,'','','',[]]
        btn=[]
        btn.append(['B1',5,10,95,'left.png','Anterior','a_PREV','Registro Anterior',''])
        btn.append(['B2',105,10,95,'right.png','Siguiente','a_NEXT','Registro Posterior',''])
        btn.append(['B3',5,70,95,'new.png','Nuevo','a_NUEVO','Nuevo Registro',''])
        btn.append(['B4',105,70,95,'save.png','Grabar','a_GRABA','Grabar Datos',''])
        btn.append(['B5',5,140,95,'delete.png','Borrar','a_BORRA','Borrar Cliente',''])
        btn.append(['B6',105,140,95,'','Listado','a_INFO:articulos','',''])
        btn.append(['B7',5,210,95,'select.png','Buscar','a_INFO:articulos,ar_ls,LS','',''])
        btn.append(['B8',105,210,95,'exit.png','Salir','a_SALIR','',''])

        p3[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(tb)
        ls_campos.append(p3)

        #P4 - Lista de Selecci�n
        p4 = ['PANEL','P4',0,400,600,170,'','','',[]]
        cols = [['Codigo','l'],['Nombre','l'],['Tipo','l'],['PVP','2'],['Stock','0']]
        ls = ['LIST','LS',0,0,-1,-1,cols,'','','','','','a_carga_rg','']
        p4[-1].append(ls)

        ls_campos.append(p4)
        #
        self.init_ctrls(ls_campos)
        #
        self._idx = 'IDX'
        self._filedb = 'articulos'
        self._accini=''      # Acci�n al cargar la ventana
        self._accleer = ''   # Acci�n despues de leer registro
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
        # Ya se ejecut� la accion. No continuar con la accion normal
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
    ventana = articulos()
    ventana.Show()
    app.MainLoop()

