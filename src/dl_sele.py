#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import OC
import pickle
from OC.Funciones import *
import os
from global_var import DIR_DATA
from global_var import DIR_APL

#
# DIALOGO DE SELECCI�N PARA CAMPOS. SE VE EL RESULTADO, SE DEVUELVE CODIGO
#
class dl_sele(OC.Dialogo):

    def __init__(self,padre,fichero,informe,entry):
        OC.Dialogo.__init__(self, padre,'Busqueda de Registros',tam=(550,650),btn=False)
        #

        # P1 - Preguntas
        p1 = ['PANEL','P1',0,0,-1,-1,'','','',[]]
        #---
        cols = []
        cols.append(['Pregunta',17,'l',0,'n','','','','','','','','',''])
        cols.append(['Op',3,'l',0,'n','','','','','','','','',''])
        cols.append(['Valor',13,'l',0,'','','','','','','','','',''])
        cols.append(['Campo',5,'l',0,'i','','','','','','','','',''])
        p1[-1].append(['GRID','G1','',5,5,350,22,7,cols,5,[],''])

        cols=[['Codigo','%'],['Nombre','l'],['Telefono','l']]
        ls = ['LIST','L1',5,265,380,140,cols,'','','','','','a_aceptar','']
        p1[-1].append(ls)

        #P1 - Botones de la Ventana
        btn=[]
        btn.append(['B1',155,215,100,'search.png','Buscar','a_buscar',''])
        btn.append(['B2',90,420,100,'good.png','Aceptar','a_aceptar',''])
        btn.append(['B3',250,420,100,'error.png','Salir','a_salir',''])
        p1[-1].append(['BUTTONS','BID',45,'','',btn])
        #
        ls_campos = []
        ls_campos.append(p1)
        #
        self.init_ctrls(ls_campos)

        #- Traemos informaci�n del informe ----------
        ls_inf = lee_dicc('forms',fichero)
        if not informe in ls_inf.keys(): return -1
        #
        deno,acc_antes,accion,acc_despues,gridc,gridp = ls_inf[informe]
        #- Contruimos preguntas con sus formatos
        lsfmt=[]
        preguntas = []
        i=0
        for ln in gridp:
            campo, titu ,fmt, lmax, op = ln
            preguntas.append([titu,op,'',campo]) #,fmt,lmax])
            lsfmt.append([fmt,i,lmax])
            i+=1

        #- Campos a mostrar
        campos=[]
        for ln in gridc:
            campos.append(ln[0])
        # -----------------------------------------------
        self._fichero = fichero
        self._campos = campos
        self._entry = entry
        # -----------------------------------------------

        grid = self._ct['G1']
        #
        for ln in lsfmt:
            fmt,fila,lmax = ln
            grid.SetFmt(fmt,2,fila)
        #
        grid.SetValue(preguntas)
        grid.SetCursor(0,2)
        #
        self.ShowModal()


    #
    #
    #
    def Ejecuta_Accion(self,accion,obj=None):

        if accion=='a_buscar':

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

            #resul.sort()
            self._ct['L1'].SetValue(resul)

        elif accion=='a_aceptar':
            res = self._ct['L1'].GetValue()
            self._entry.SetValue(res)
            self._res = res
            self.Close()

        elif accion=='a_salir':
            self._res = None
            self.Close()

    #
    #
    #
    def res(self):
        res =self._res
        self.Destroy()
        return res


#############################################
#
#
#############################################
if __name__ == "__main__":
    app = wx.PySimpleApp()
    #frame = wx.Frame(None,title="Prueba de la Clase Grid")
    #frame.SetSize((800,600))
    #frame.CentreOnScreen()

    fichero = 'clientes'
    preguntas = []
    preguntas.append(['Nombre del Cliente','=','','CL_DENO'])
    preguntas.append(['Poblacion','=','','CL_POB'])

    dl = dl_sele(None,fichero, preguntas)
    res = dl.res()
    debug(res)

    app.MainLoop()
