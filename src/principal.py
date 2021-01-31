#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os
import OC
from OC.Funciones import Men
from OC.Funciones import debug


class Principal(OC.Ventana):
    """ Ventana para seleccionar ejercicio de trabajo """
    
    def __init__(self):
        OC.Ventana.__init__(self, None,'Seleccione Ejercicio',tam=(400,300))
        #
        ls_campos = []
        #
        p1 = ['PANEL','P1',0,0,-1,200,'',[]]
        #---
        hp1=[]  # hijos de P1
        cols=[['Ejercicio','l']]
        ls1 = ['LIST','L1',2,2,390,190,cols,'','a_entra']
        hp1.append(ls1)
        p1[-1]=hp1
        ls_campos.append(p1)
        #
        p2 = ['PANEL','P2',0,200,-1,70,'',[]]
        
        btn=[]
        btn.append(['B1',(100,20),80,'','ENTRAR','a_entra','Entrar en el Ejercicio'])
        btn.append(['B2',(200,20),80,'salir.png','SALIR','a_SALIR',''])
        #
        p2[-1].append(['BUTTONS',40,'','',btn])
        
        ls_campos.append(p2)
        #
        self.init_ctrls(ls_campos)
        #
        self._ct['L1'].SetAnchos([100])
        #
        lsdir = os.listdir(OC.Funciones.DIR_DATA)
        if lsdir==[]:
            Men('No hay ejercicios definidos.')
        else:
            xxx=[]
            for ej in lsdir: xxx.append([ej])
            self._ct['L1'].SetValue(xxx)
    
    #
    #
    #
    def Ejecuta_Accion(self,accion):
        """ Acciones a ejecutar """
        
        # Probamos primero si es una accion estandar
        std = OC.Ventana.Ejecuta_Accion(self, accion)
        # Ya se ejecutó la accion. No continuar con la accion normal
        if std<>-999: return 
        
        if accion=='a_entra':
            eja = self._ct['L1'].GetValue()
            if eja=='':
                Men('No ha seleccionado ningun ejercicio')
                return
            
            OC.Funciones.DIR_DATA += '\\' + eja
            
            import inicio
            self.Show(0)
            inicio.Inicio(self)


    
#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    import wx 
    
    app = wx.PySimpleApp()
    ventana = Principal()
    app.MainLoop()

        