#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx
import OC
import pickle
from OC.Funciones import *

class tecnicos(OC.Ventana):
    """ Ficha para manejar las ventanas de la aplicación """

    def __init__(self,padre=None):
        OC.Ventana.__init__(self, padre,'Técnicos',tam=(800,600))
        #
        ls_campos = []

        # TABBOX
        tb = ['TABBOX','TBG',0,0,600,400,'','','a_cambia_tab',[]]

        # PN1 - Pestaña General
        pn1 = ['PANEL','PN1',0,0,-1,-1,'','','General',[]]
        #cols=[['Ventana','l'],['Descripción','l']]
        #ls = ['LIST','L1',0,0,-1,-1,cols,'','','','','a_sele_win','','']
        #p0[-1].append(ls)
        eng = ['ENTRYS','ENG','25','50','','',[]]
        #eng[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        eng[-1].append(['IDX','Codigo','5','20','6','%','3','','','','a_LEE_RG','','','',''])
        eng[-1].append(['TN_DENO','Nombre Técnico','-1','','50','l','100','','','','','','','',''])
        eng[-1].append(['TN_DOM','Dirección','-1','','57','l','100','','','','','','','',''])
        eng[-1].append(['TN_CP','CPostal','-1','','7','l','5','','','','','','','',''])
        eng[-1].append(['TN_POB','Población','-1','','30','l','100','','','','','','','',''])
        eng[-1].append(['TN_PROV','Provincia','-1','','13','l','100','','','','','','','',''])
        eng[-1].append(['TN_TFN','Telefonos','-1','','20','l','30','','','','','','','',''])
        eng[-1].append(['TN_FNAC','F. Nacimiento','-1','','10','d','10','','','','','','','',''])
        eng[-1].append(['TN_FALT','Fecha Alta','-1','','10','d','10','','','','','','','',''])
        eng[-1].append(['TN_FBJA','Fecha Baja','-1','','10','d','10','','','','','','','',''])
        pn1[-1].append(eng)
        tb[-1].append(pn1)


        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',600,200,200,370,'','','',[]]
        btn=[]
        btn.append(['B1',5,10,95,'left.png','Anterior','a_PREV','Registro Anterior',''])
        btn.append(['B2',105,10,95,'right.png','Siguiente','a_NEXT','Registro Posterior',''])
        btn.append(['B3',5,70,95,'new.png','Nuevo','a_NUEVO','Nuevo Registro',''])
        btn.append(['B4',105,70,95,'save.png','Grabar','a_GRABA','Grabar Datos',''])
        btn.append(['B5',5,140,95,'delete.png','Borrar','a_BORRA','Borrar Registro',''])
        btn.append(['B6',105,140,95,'report.png','Listado','a_INFO','',''])
        btn.append(['B7',5,210,95,'select.png','Buscar','a_INFO:tecnicos,tn_ls,LS','',''])
        btn.append(['B8',105,210,95,'exit.png','Salir','a_SALIR','',''])
        p3[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(tb)
        ls_campos.append(p3)

        #P4 - Lista de Selección
        p4 = ['PANEL','P4',0,400,600,170,'','','',[]]
        cols = [['Codigo','l'],['Nombre','l'],['Telefono','l']]
        ls = ['LIST','LS',0,0,-1,-1,cols,'','','','','','a_carga_rg','']
        p4[-1].append(ls)

        ls_campos.append(p4)
        #
        self.init_ctrls(ls_campos)
        #
        self._idx = 'IDX'
        self._filedb = 'tecnicos'
        self._accini=''      # Acción al cargar la ventana
        self._accleer = ''   # Acción despues de leer registro
        self._btfin = ''     # Nombre del boton a ejecutar cuando pulse boton FIN


    #
    #-- Acciones a ejecutar
    #
    def Ejecuta_Accion(self,accion,obj=None,args=None):

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

        elif accion=='a_inf1':
            res,preguntas = args

            lsav = select('alb-venta','0 AV_TN AV_TTT',preguntas)

            dc={}
            for ln in lsav:
                cdav,cdtn,ttt =ln[:3]
                if not cdtn in dc.keys(): dc[cdtn]=[0,0] # num,ttt
                dc[cdtn][0]+=1
                dc[cdtn][1]+=ttt

            #
            rs=[]
            for cdtn in dc.keys():
                num,ttt = dc[cdtn]
                tn = lee('tecnicos',cdtn)
                if tn==1: deno='NO DEFINIDO'
                else: deno=tn['TN_DENO']
                rs.append([cdtn,deno,num,ttt])

            return rs

        return 0


#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App(False)
    ventana = tecnicos()
    ventana.Show()
    app.MainLoop()

