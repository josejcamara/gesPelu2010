#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import OC.Dialogo
import pickle
from OC.Funciones import *

class Detalle_Buttons(OC.Dialogo.Dialogo):
    """ Dialgo para manejar las propiedades de las entradas"""
    def __init__(self,padre=None):
        OC.Dialogo.Dialogo.__init__(self, padre,'Detalle Entradas',tam=(800,300))
        #

        # P2 - Propiedades del Objeto
        p2 = ['PANEL','P2',0,0,-1,-1,'','','',[]]
        #---
        cols = []
        cols.append(['Id',3,'l',0,'','','','','','','','','',''])
        cols.append(['X',3,'l',0,'','','','','','','','','',''])
        cols.append(['Y',3,'l',0,'','','','','','','','','',''])
        cols.append(['Ancho',4,'l',0,'','','','','','','','','',''])
        cols.append(['Imagen',15,'l',0,'','','','','','','','','',''])
        cols.append(['Texto',15,'l',0,'','','','','','','','','',''])
        cols.append(['Accion',14,'l',0,'','','','','','','','','',''])
        cols.append(['Tip Ayuda',15,'l',0,'','','','','','','','','',''])
        cols.append(['Tecla',4,'l',0,'','','','','','','','','',''])
        #
        p2[-1].append(['GRID','G1','Titulo',5,5,785,22,7,cols,1,[],''])
        
        #P3 - Botones de la Ventana
        btn=[]    
        btn.append(['B1',210,210,80,'save.png','Grabar','a_graba',''])
        btn.append(['B2',510,210,80,'salir.png','Salir','a_salir',''])
        p2[-1].append(['BUTTONS','BID',50,'','',btn])
        
        #
        ls_campos = []
        ls_campos.append(p2)
        #
        self.init_ctrls(ls_campos)
        
        #---
        self.Ejecuta_Accion('a_carga_wins')
        
    #
    #
    #
    def Ejecuta_Accion(self,accion):
        if accion=='a_salir':
            if self.Modifica==1:
                dlg = Men('Hay cambios en la ventana y no ha guardado.\n¿Desea Continuar?','sn',img='q')
                if dlg=='n': return
            self.Modifica = 0
            self.Close()
            self.Destroy()
            #
        
#############################################
#
#
#############################################
if __name__ == "__main__":
    app = wx.PySimpleApp()
    #frame = wx.Frame(None,title="Prueba de la Clase Grid")
    #frame.SetSize((800,600))
    #frame.CentreOnScreen()
    frame = Detalle_Buttons()
    
    app.MainLoop()
