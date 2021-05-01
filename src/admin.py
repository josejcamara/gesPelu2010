#!/usr/bin/env python
# -*- coding: utf-8 -*-

import OC
from OC.Funciones import *

import wx, shutil
import os
import os.path
import datetime

class AdminApp(OC.Ventana):
    """ Administracion de la aplication """

    def __init__(self,padre=None):
        OC.Ventana.__init__(self, padre,'Administrar Aplicacion',tam=(490,250))

        ls_campos = []
        #
        p1 = ['PANEL','P1',0,0,500,300,'',[]]
        #---
        hp1=[]  # hijos de P1
        #
        btn=[]
        # btn.append(['B1',10,10,110,'','Ventanas','a_abre_EdiWin','Editar Ventanas'])  # Not in use
        btn.append(['B2',130,10,110,'','Tablas','a_abre_EdiDicc','Editar Tablas'])
        btn.append(['B3',250,10,110,'','Reports','a_abre_EdiForm','Editar Informes'])
        #
        btn.append(['BTSALIR',200,185,100,'exit.png','Salir','a_SALIR','Salir del programa'])
        #
        hp1.append(['BUTTONS','BTI',50,'','',btn])
        p1[-1] = hp1
        #
        ls_campos.append(p1)
        #
        self.init_ctrls(ls_campos)
        #


    #
    #-- Acciones a ejecutar
    #
    def Ejecuta_Accion(self,accion,obj=None,args=None):

        ''' Acciones a ejecutar '''
        # Probamos primero si es una accion estandar
        std = OC.Ventana.Ejecuta_Accion(self, accion,obj)
        ok,val = std

        # Comprobar el valor devuelto por si hay que hacer algo
        # Ya se ejecutó la accion. No continuar con la accion normal
        if ok>0:
            return val

        if accion == 'a_abre_EdiWin':
            import EdiWin
            win = EdiWin.Manage_Win()
        elif accion == 'a_abre_EdiDicc':
            import EdiDicc
            win = EdiDicc.Manage_Dicc('dicc')
        elif accion == 'a_abre_EdiForm':
            import EdiForm
            win = EdiForm.Manage_Form('forms')



#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = AdminApp()
    return win

#----------------------------------------------------------------------

#############################################################
#
#
##############################################################
if __name__ == "__main__":
    # import global_var

    app = wx.App(False)

    ventana = AdminApp()
    app.MainLoop()
