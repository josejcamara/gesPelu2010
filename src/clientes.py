#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import OC
import pickle
from OC.Funciones import *


class clientes(OC.Ventana):
    """ Ficha para manejar las ventanas de la aplicación """

    def __init__(self,padre=None):
        OC.Ventana.__init__(self, padre,'Clientes',tam=(800,600))
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
        eng[-1].append(['IDX','Código','5','20','6','%','6','','','','a_LEE_RG|a_pon_histo','','','',''])
        eng[-1].append(['CL_DENO','Nombre Cliente','-1','','50','l','100','','','','','','','',''])
        eng[-1].append(['CL_DOM','Dirección','-1','','57','l','100','','','','','','','',''])
        eng[-1].append(['CL_CP','CPostal','-1','','7','l','5','','','','','','','',''])
        eng[-1].append(['CL_POB','Población','-1','','30','l','100','','','','','','','',''])
        eng[-1].append(['CL_PROV','Provincia','-1','','13','l','100','','','','','','','',''])
        eng[-1].append(['CL_TFN','Telefonos','-1','','20','l','30','','','','','','','',''])
        eng[-1].append(['CL_FALT','Fecha Alta','-1','','10','d','10','','','','','','','',''])
        eng[-1].append(['CL_FNAC','F. Nacimiento','-1','','10','d','10','','','','','','','',''])
        pn1[-1].append(eng)
        tb[-1].append(pn1)

        # PN2 - Datos Tecnicos
        pn2 = ['PANEL','PN2',200,0,600,500,'','','Técnico',[]]
        ent = ['ENTRYS','ENT','25','50','','',[]]
        ent[-1].append(['CL_DTEC','Datos Técnicos','5','20','57','m13','','','','','','','','',''])
        #
        pn2[-1].append(ent)
        tb[-1].append(pn2)

        # PN3 - Historia Citas
        pn3 = ['PANEL','PN3',200,0,600,500,'','','Histórico',[]]
        cols=[['Nº Venta','l'],['Fecha','d'],['Tecnico','l'],['Importe','2']]
        ls = ['LIST','L1',10,10,580,210,cols,'','','','','a_pon_detalle','','']
        pn3[-1].append(ls)
        #
        cols=[['Articulo','l'],['Nombre Articulo','l'],['Unidades','2']]
        ls = ['LIST','L2',10,230,580,110,cols,'','','','','','','']
        pn3[-1].append(ls)
        #
        tb[-1].append(pn3)


        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',600,200,200,370,'','','',[]]
        btn=[]
        btn.append(['B1',5,10,90,'left.png','Anterior','a_PREV','Registro Anterior',''])
        btn.append(['B2',105,10,90,'right.png','Siguiente','a_NEXT','Registro Posterior',''])
        btn.append(['B3',5,70,90,'new.png','Nuevo','a_NUEVO','Nuevo Cliente',''])
        btn.append(['B4',105,70,90,'save.png','Grabar','a_GRABA','Grabar Datos',''])
        btn.append(['B5',5,140,90,'delete.png','Borrar','a_BORRA','Borrar Cliente',''])
        btn.append(['B6',105,140,90,'report.png','Listado','a_INFO:clientes','Informes y Listados',''])
        btn.append(['B7',5,210,90,'select.png','Buscar','a_INFO:clientes,cl_ls,LS','',''])
        btn.append(['B8',105,210,90,'exit.png','Salir','a_SALIR','',''])
        p3[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(tb)
        ls_campos.append(p3)

        #P4 - Lista de Selección
        p4 = ['PANEL','P4',0,400,600,170,'','','',[]]
        cols = [['Código','l'],['Nombre','l'],['Telefono','l'],['Población','l']]
        ls = ['LIST','LS',0,0,-1,-1,cols,'','','','','','a_carga_rg','']
        p4[-1].append(ls)

        ls_campos.append(p4)
        #
        self.init_ctrls(ls_campos)
        #
        self._idx = 'IDX'
        self._filedb = 'clientes'
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

        elif accion=='a_pon_histo':
            cdcl = self._ct['IDX'].GetValue()
            histo = select('alb-venta','0 AV_FEC AV_TN AV_TTT',[['AV_CL','=',cdcl]])
            self._ct['L1'].SetValue(histo)


        elif accion=='a_pon_detalle':
            resul = []
            cdav = self._ct['L1'].GetValue()
            av = lee('alb-venta',cdav)
            for ln in av['AV_LNA']:
                cdar,uds = ln[:2]
                ar = lee('articulos',cdar)
                if ar==1: continue
                resul.append([cdar,ar['AR_DENO'],uds])
            self._ct['L2'].SetValue(resul)


        elif accion=='a_inf1':
            res,preguntas = args

            mes=0
            for ln in preguntas:
                if ln[0]=='MES': mes=ln[2]

            rs=[]
            for cdcl in res:
                cli = lee('clientes',cdcl)
                if cli==1: continue
                fnac = cli['CL_FNAC']
                if mes<>0 and mes <> Num_aFecha(fnac,'m'): continue
                rs.append([cdcl,cli['CL_DENO'],cli['CL_FNAC'],cli['CL_DOM'],cli['CL_CP'],cli['CL_POB']])

            return rs

        elif accion=='a_inf2':
            res,preguntas = args
            ls_cl=res

            prg=[]
            for ln in preguntas:
                if ln[0]=='DFEC': prg.append(['AV_FEC','>=',ln[2]])
                if ln[0]=='HFEC': prg.append(['AV_FEC','<=',ln[2]])
            #
            rs=[]
            vtas = select('alb-venta','0 AV_CL AV_TTT AV_COB AV_FEC',prg)
            for ln in vtas:
                cdav,cdcl,ttt,cob,av_fec = ln[:5]
                if not cdcl in ls_cl: continue  # Cliente no preguntado
                if ttt<>cob:
                    cli = lee('clientes',cdcl)
                    if cli==1: denocli = 'NO DEFINIDO'
                    else: denocli = cli['CL_DENO']
                    rs.append([cdcl,denocli,cdav,av_fec,ttt,cob,ttt-cob])

            rs.sort()
            return rs

        return 0


#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App()
    ventana = clientes()
    ventana.Show()
    app.MainLoop()

