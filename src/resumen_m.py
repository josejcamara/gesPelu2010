#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx
import wx.lib.calendar
import OC
import os

from OC.Funciones import *

class resumen_m(OC.Ventana):
    """ Agenda de Citas """

    def __init__(self,padre=None):

        OC.Ventana.__init__(self, padre,'Resumen Ventas',tam=(760,530))
        #
        ls_campos = []

        p2 = ['PANEL','P2',1,1,730,525,'','1','',[]]
        titulos = ['Fecha','Servicios','Productos','Total','Gastos','Beneficio']
        cols = []
        cols.append(['Fecha',8,'d',0,'','','','','','','','','',''])
        cols.append(['Servicios',8,'2',0,'','','','','','','','','',''])
        cols.append(['Productos',9,'2',0,'','','','','','','','','',''])
        cols.append(['Ingresos',8,'2',0,'','','','','','','','','',''])
        cols.append(['Gastos',8,'2',0,'','','','','','','','','',''])
        cols.append(['Beneficio',8,'2',0,'','','','','','','','','',''])
        #
        p2[-1].append(['GRID','G_DIAS','',2,5,515,20,22,cols,0,[],''])

        e1 = ['ENTRYS','EN1','25','50','','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        e1[-1].append(['TT1','','80','485','8','2','10','n','','','','','','',''])
        e1[-1].append(['TT2','','162','485','9','2','10','n','','','','','','',''])
        e1[-1].append(['TT3','','252','485','8','2','10','n','','','','','','',''])
        e1[-1].append(['TT4','','332','485','8','2','10','n','','','','','','',''])
        e1[-1].append(['TT5','','412','485','8','2','10','n','','','','','','',''])
        p2[-1].append(e1)

        e2 = ['ENTRYS','EN2','25','50','','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        e2[-1].append(['DFEC','Desde Fecha','530','50','9','d','10','','','','','','','',''])
        e2[-1].append(['HFEC','Hasta Fecha','630','50','9','d','10','','','','','','','',''])
        e2[-1].append(['RATIO','[% Ajuste','600','80','8','2','10','','','','','','','',''])
        e2[-1].append(['NADA','','600','580','6','l','10','','','','','','','',''])
        p2[-1].append(e2)

        btn=[]
        btn.append(['B9',575,150,95,'refresh.png','','a_actu_resumen','Actualizar Resumen',''])
        p2[-1].append(['BUTTONS','BID',50,'','',btn])


        btn=[]
        btn.append(['B4',530,450,95,'save.png','Guardar','a_guarda_resumen','Crear fichero para contable',''])
        btn.append(['B8',630,450,95,'exit.png','Salir','a_SALIR','',''])
        p2[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(p2)

        #
        self._idx = ''
        self._filedb = ''
        self._accini=''      # Acci�n al cargar la ventana
        self._accleer = ''   # Acci�n despues de leer registro
        self._btfin = ''     # Nombre del boton a ejecutar cuando pulse boton FIN
        #
        self.init_ctrls(ls_campos)
        #
        #self.Ejecuta_Accion(self._accini)


    #
    #-- Acciones a ejecutar
    #
    def Ejecuta_Accion(self,accion,obj=None):
        pb = self

        """ Acciones a ejecutar """
        # Probamos primero si es una accion estandar
        std = OC.Ventana.Ejecuta_Accion(self, accion,obj)
        ok,val = std

        # Comprobar el valor devuelto por si hay que hacer algo
        # Ya se ejecut� la accion. No continuar con la accion normal
        if ok>0:
            return val

        if accion=='a_ini_var':
            pb._ct['IDX'].SetValue(Fecha())
            self.Modifica=0

        elif accion=='a_actu_resumen':
            dfec=pb._ct['DFEC'].GetValue()
            hfec=pb._ct['HFEC'].GetValue()
            porcen = pb._ct['RATIO'].GetValue()

            if hfec==None: hfec=Fecha()

            if dfec==None or hfec==None:
                Men('Debe indicar el rango de fechas.')
                return -1
            if porcen==0: porcen = 100.

            resul = []
            dc={}
            #
            #-- RECORRIDO DEL FICHERO ANTIGUO !!!
            #
            cods = select('diario','0',[['0','>=',dfec],['0','<=',hfec]])
            for cod in cods:
                rg = lee('diario',cod)
                cod = int(cod)
                srv = rg['DC_SRV']
                vta = rg['DC_VTS']
                gas = rg['DC_GAS']
                #
                ttsrve,ttsrvj = 0,0     # Total Servicios Efectivo, Tarjeta
                ttvtse,ttvtsj = 0,0     # Total Ventas Efectivo, Tarjeta
                ttgas = 0               # Total Gastos
                for ln in srv:
                    if ln[1]=='':continue   # Sin importe??
                    impo = float(ln[1])
                    if ln[2] in ('s','S'): ttsrvj += impo
                    else: ttsrve += impo
                for ln in vta:
                    if ln[1]=='':continue   # Sin importe??
                    impo = float(ln[1])
                    if ln[2] in ('s','S'): ttvtsj += impo
                    else: ttvtse += impo
                for ln in gas:
                    if ln[1]=='':continue   # Sin importe??
                    impo = float(ln[1])
                    ttgas += impo
                #
                fec = cod
                dc[fec] = [ttsrve,ttsrvj,ttvtse,ttvtsj,ttgas]

            #
            #-- VALORES DE LAS FICHAS NUEVAS
            ## NO COGEMOS COBROS PQ NO TENEMOS FORMA DE SABER A QUE ARTICULO PERTENECE EL IMPORTE !!!!!!
            #
            cods = select('alb-venta','0',[['AV_FEC','>=',dfec],['AV_FEC','<=',hfec]])
            for cd in cods:
                av = lee('alb-venta',cd)
                estj = av['AV_PTJ']
                lnas = av['AV_LNA']
                fec = av['AV_FEC']
                if not fec in dc.keys(): dc[fec]=[0,0,0,0,0]
                for ln in lnas:
                    cdar,uds,pvp = ln[:3]
                    ar=lee('articulos',cdar)
                    if ar==1: tipo='P'
                    else: tipo = ar['AR_TIPO']
                    if tipo=='S':
                        if not estj: dc[fec][0]+=uds*pvp    # Servicio Efectivo
                        else: dc[fec][1]+= uds*pvp      # Servicio Tarjeta
                    else:
                        if not estj: dc[fec][2]+=uds*pvp    # Producto Efectivo
                        else: dc[fec][3]+= uds*pvp      # Producto Tarjera

            ls_ga = select('gastos','0 GA_IMPO GA_FEC',[['GA_FEC','>=',dfec],['GA_FEC','<=',hfec]])
            for ln in ls_ga:
                cod,impo,fec = ln
                if not fec in dc.keys(): dc[fec]=[0,0,0,0,0]
                dc[fec][4]+= impo

            #
            tt1,tt2,tt3 = 0,0,0
            hoja=[]
            for fec in dc:
                ttsrve,ttsrvj,ttvtse,ttvtsj,ttgas = dc[fec]
                ttsrv = round(ttsrvj + ttsrve*porcen/100.,2)
                ttvts = round(ttvtsj + ttvtse*porcen/100.,2)
                hoja.append([fec,ttsrv,ttvts,ttsrv+ttvts,ttgas,ttsrv+ttvts-ttgas])
                tt1+=ttsrv
                tt2+=ttvts
                tt3+=ttgas

            #
            hoja.sort()
            ##hoja.append([None,tt1,tt2,tt1+tt2,tt3,tt1+tt2-tt3])
            pb._ct['G_DIAS'].SetValue(hoja)
            pb._ct['TT1'].SetValue(tt1)
            pb._ct['TT2'].SetValue(tt2)
            pb._ct['TT3'].SetValue(tt1+tt2)
            pb._ct['TT4'].SetValue(tt3)
            pb._ct['TT5'].SetValue(tt1+tt2-tt3)


        #
        #--
        #
        elif accion=='a_guarda_resumen':
            hoja = pb._ct['G_DIAS'].GetValue()
            titus = ['Fecha','Servicios','Productos','Total','Gastos','Beneficio']

            SEP = '\t'
            aux = []
            for ln in hoja:
                ln[0] = Num_aFecha(ln[0])
                ln[1],ln[2],ln[3] = str(ln[1]),str(ln[2]),str(ln[3])
                ln[4],ln[5] = str(ln[4]),str(ln[5])
                for i in range(len(ln)): ln[i] = ln[i].replace('.',',')
                aux.append(SEP.join(ln))
            hoja= '\n'.join(aux)
            titus = '\t'.join(titus)
            hoja = titus + '\n' + hoja

            ## Seleccionar Directorio
            dlg = wx.DirDialog(self,"Elija Directorio",
                defaultPath=os.environ['HOME'],
                style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
            ruta = ''
            if dlg.ShowModal()==wx.ID_OK:
                ruta = dlg.GetPath()
            dlg.Destroy()
            ##
            if ruta=='':
                Men('Proceso Cancelado. No ha indicado donde guardar.')
                return -1

            dfec=pb._ct['DFEC'].GetValue()
            hfec=pb._ct['HFEC'].GetValue()
            dfec = Num_aFecha(dfec).replace('/','_')
            hfec = Num_aFecha(hfec).replace('/','_')
            ruta += '/resumen_'+dfec+'-'+hfec+'.xls'
            f = open(ruta,"wb")
            f.write(hoja)
            f.close()
            Men('Resumen creado correctamente.')


        return 0 # No se ejecut� ninguna accion !!!!



#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App(False)
    ventana = resumen_m()
    ventana.Show()
    app.MainLoop()
