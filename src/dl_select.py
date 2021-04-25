#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx
import OC
import pickle
from OC.Funciones import *
import os
from global_var import DIR_DATA
from global_var import DIR_APL

#
# DIALOGO DE SELECCIÓN PARA INFORMES. NO SE VE EL RESULTADO SE VE INFORME.
#
class dl_select(OC.Dialogo):
    """ Dialogo de selección de registros, pone en lista destino """
    #def __init__(self,padre,inf):
    def __init__(self,padre,fichero,campos,preguntas):
        OC.Dialogo.__init__(self, padre,'Selección de Registros',tam=(580,520),btn=False)
        #
        preg=[]
        lsfmt=[]
        i=0
        for ln in preguntas:
            titu,op,valor,campo,fmt,lmax = ln
            preg.append([titu,op,valor,campo])
            lsfmt.append([fmt,i,lmax])
            i+=1

        self._fichero = fichero
        self._preguntas = preg
        self._campos = campos
        self._res = None
        self._prg = []

        # P1 - Preguntas
        p1 = ['PANEL','P1',0,0,-1,-1,'','','',[]]
        #---
        cols = []
        cols.append(['Pregunta',17,'l',0,'n','','','','','','','','',''])
        cols.append(['Op',3,'l',0,'n','','','','','','','','',''])
        cols.append(['Valor',13,'l',0,'','','','','','','','','',''])
        cols.append(['Campo',5,'l',0,'i','','','','','','','','',''])
        #
        p1[-1].append(['GRID','G1','Búsqueda Selectiva',10,10,370,22,7,cols,1,[],''])


        #P1 - Botones de la Ventana
        btn=[]
        btn.append(['B2',90,290,100,'good.png','Aceptar','a_aceptar',''])
        btn.append(['B3',250,290,100,'error.png','Salir','a_salir',''])
        p1[-1].append(['BUTTONS','BID',45,'','',btn])
        #
        ls_campos = []
        ls_campos.append(p1)
        #
        self.init_ctrls(ls_campos)
        #
        grid = self._ct['G1']
        #
        for ln in lsfmt:
            fmt,fila,lmax = ln
            grid.SetFmt(fmt,2,fila)

        grid.SetValue(preguntas)
        grid.SetCursor(0,2)
        #
        self.ShowModal()


    #
    #
    #
    def Ejecuta_Accion(self,accion,obj=None):

        if accion=='a_aceptar':
            fichero = self._fichero
            campos = self._campos
            preguntas = self._ct['G1'].GetValue()
            #
            preg=[]
            for lnp in preguntas:
                deno,op,valor,campo= lnp
                if valor in ['',None,0]: continue
                preg.append([campo,op,valor])
            #
            resul = select(fichero,campos,preg)
            resul.sort()
            self._res = resul
            self._prg = preg
            self.Close()

        elif accion=='a_salir':
            self._res = None
            self._prg = []
            self.Close()

        return 1
    #
    #
    #
    def res(self):
        res = self._res
        prg = self._prg
        self.Destroy()
        return (res,prg)



class dl_sel_inf(OC.Dialogo):
    """ Dialogo de selección de informes """
    def __init__(self,padre,fichero):
        OC.Dialogo.__init__(self, padre,'Seleccion de Informes',tam=(550,600))
        #

        # P1 -
        p1 = ['PANEL','P1',0,0,-1,300,'','','',[]]
        #---
        cols = [['Informe','l'],['Descripción','l']]
        ls = ['LIST','LS',5,5,390,290,cols,'','','','','','','']
        p1[-1].append(ls)
        #
        ls_campos = [p1]
        #
        self.init_ctrls(ls_campos)
        #
        ls_inf = lee_dicc('forms',fichero)
        lis=[]

        for key in ls_inf.keys():
            deno_info = ls_inf[key][0]
            lis.append([key,deno_info])
        self._ct['LS'].SetValue(lis)
        #
        #self.ShowModal()   # Lo hace en el res()

    def res(self):
        if self.ShowModal()== wx.ID_OK:
            res = self._ct['LS'].GetValue()
        else:
            res = None

        self.Close()
        self.Destroy()
        return res


#############################################
#
#
#############################################
if __name__ == "__main__":
    app = wx.App(False)
    #frame = wx.Frame(None,title="Prueba de la Clase Grid")
    #frame.SetSize((800,600))
    #frame.CentreOnScreen()

    fichero = 'clientes'
    preguntas = []
    preguntas.append(['Nombre del Cliente','=','','CL_DENO'])
    preguntas.append(['Poblacion','=','','CL_POB'])

    dl = dl_select(None,fichero, preguntas)
    res = dl.res()
    debug('res Main',res)

    app.MainLoop()
