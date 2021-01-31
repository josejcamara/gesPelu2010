#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import wx.calendar
import OC
import os
from OC.Funciones import *


class diario(OC.Ventana):
    """ Ficha para manejar las ventanas de la aplicación """

    def __init__(self,padre=None):

        OC.Ventana.__init__(self, padre,'Diario de Ingresos y Gastos',tam=(800,540))
        #
        ls_campos = []

        # Panel para el calendario
        p1 = ['PANEL','P1',0,0,350,185,'','','',[]]
        enf = ['ENTRYS','ENG','25','50','','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        enf[-1].append(['IDX','Fecha','260','140','9','d','10','n','','','a_LEE_RG:n','','','',''])
        p1[-1].append(enf)
        #
        ls_campos.append(p1)

        # TABBOX
        tb = ['TABBOX','TBG',0,185,600,350,'','','',[]]

        # PN1 - Ventas de Servicios
        pn1 = ['PANEL','PN1',10,10,500,300,'','','Servicios',[]]
        #---
        cols = []
        cols.append(['Descripción',37,'l',0,'','','','','','','','','',''])
        cols.append(['Importe',8,'2',0,'','','','','','','','','',''])
        cols.append(['Tarj',5,'l',1,'','','','','a_SELE:s+S+|a_pon_tt','LISTA:S-Tarjeta]1','','','',''])
        #
        pn1[-1].append(['GRID','DC_SRV','Ventas',5,5,590,22,11,cols,0,'',''])
        #
        tb[-1].append(pn1)

        # PN2 - Ventas de Productos
        pn2 = ['PANEL','PN2',10,10,500,300,'','','Ventas',[]]
        #---
        cols = []
        cols.append(['Descripción',37,'l',0,'','','','','','','','','',''])
        cols.append(['Importe',8,'2',0,'','','','','','','','','',''])
        cols.append(['Tarj',5,'l',1,'','','','','a_SELE:s+S+|a_pon_tt','LISTA:S-Tarjeta]1','','','',''])
        #
        pn2[-1].append(['GRID','DC_VTS','Ventas',5,5,590,22,11,cols,0,'',''])
        #
        tb[-1].append(pn2)

        # PN3 - Compras /Gastos
        pn3 = ['PANEL','PN3',200,0,600,500,'','','Compras',[]]
        #---
        cols = []
        cols.append(['Descripción',40,'l',0,'','','','','','','','','',''])
        cols.append(['Importe',10,'2',0,'','','','','','','','','',''])
        #
        pn3[-1].append(['GRID','DC_GAS','Gastos',5,5,590,22,11,cols,0,'',''])
        #
        tb[-1].append(pn3)

        # PN4 - Resumen del Día
        pn4 = ['PANEL','PN4',200,0,600,500,'','','Resumen',[]]
        #---
        e2 = ['ENTRYS','EN2','25','50','','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        e2[-1].append(['DC_CINI','[Caja Inicial','100','10','9','2','10','','','','','','','',''])
        e2[-1].append(['DC_CHOY','[Hoy','100','50','9','2','10','','','','','','','',''])
        e2[-1].append(['DC_CFIN','[Caja Final','100','90','9','2','10','','','','','','','',''])
        e2[-1].append(['DC_CDES','[Descuadre','100','130','9','2','10','','','','','','','',''])
        pn4[-1].append(e2)
        btn=[]
        btn.append(['B9',230,70,95,'refresh.png','','a_actu_resumen','Actualizar Resumen',''])
        pn4[-1].append(['BUTTONS','BID',50,'','',btn])
        #
        tb[-1].append(pn4)


        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',600,185,200,385,'','','',[]]
        btn=[]
        btn.append(['B4',5,70,95,'save.png','Grabar','a_GRABA','Grabar Diario',''])
        btn.append(['B5',105,70,95,'delete.png','Borrar','a_BORRA','Borrar Diario',''])
        btn.append(['B6',5,130,195,'stats.png','Resumen Mensual','a_genera_archivo','Generar Archivo Contable',''])
        btn.append(['B8',105,210,95,'exit.png','Salir','a_SALIR','',''])
        p3[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(tb)
        ls_campos.append(p3)



        self._idx = 'IDX'
        self._filedb = 'diario'
        self._accini='a_ini_var'      # Acción al cargar la ventana
        self._accleer = ''   # Acción despues de leer registro
        self._btfin = ''     # Nombre del boton a ejecutar cuando pulse boton FIN
        #
        self.init_ctrls(ls_campos)
        #
        self.cal = wx.calendar.CalendarCtrl(date=wx.DateTime.Now(),
            parent=self._ct['P1'],pos=wx.Point(0,0),style=wx.calendar.CAL_SHOW_HOLIDAYS|wx.calendar.CAL_MONDAY_FIRST)
        self.cal.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED,self.OnCalSelected)
        #
        self.Ejecuta_Accion(self._accini)

    #
    #-- FUNCIONES DEL CALENDARIO
    #
    def OnCalSelected(self, evt):
        sele = evt.Date
        text = "%02d/%02d/%d" % (sele.GetDay(), sele.GetMonth()+1, sele.GetYear())
        self._ct['IDX'].SetValue(Fecha_aNum(text))


    #
    #-- FIN FUNCIONES CALENDARIO
    #

    #
    #-- Acciones a ejecutar
    #
    def Ejecuta_Accion(self,accion,obj=None):
        """ Acciones a ejecutar """
        # Probamos primero si es una accion estandar
        std = OC.Ventana.Ejecuta_Accion(self, accion,obj)
        ok,val = std

        # Comprobar el valor devuelto por si hay que hacer algo
        # Ya se ejecutó la accion. No continuar con la accion normal
        if ok>0:
            return val

        pb = self
        ct = pb._ct

        try:
            if accion=='a_ini_var':
                pb._ct['IDX'].SetValue(Fecha())

            elif accion=='a_actu_resumen':
                inicio = ct['DC_CINI'].GetValue()
                fin = ct['DC_CFIN'].GetValue()
                hoy = 0
                for ln in ct['DC_SRV'].GetValue():
                    if not ln[2] in ('s','S'):
                        if ln[1]=='': ln[1]='0'
                        impo = float(ln[1])
                        hoy += impo
                for ln in ct['DC_VTS'].GetValue():
                    if not ln[2] in ('s','S'):
                        if ln[1]=='': ln[1]='0'
                        impo = float(ln[1])
                        hoy += impo
                for ln in ct['DC_GAS'].GetValue():
                    if ln[1]=='': ln[1]='0'
                    impo = float(ln[1])
                    hoy -= impo

                ct['DC_CHOY'].SetValue(hoy)
                descuadre = inicio+hoy-fin
                descuadre = -1*descuadre
                ct['DC_CDES'].SetValue(descuadre)


            elif accion=='a_genera_archivo':
                ## DIALOGO CON PREGUNTAS DE SELECCIÓN
                lsc = []
                p1 = ['PANEL','P1',0,0,-1,-1,'','','',[]]
                enf = ['ENTRYS','FECS','25','50','','',[]]
                #enf[-1].append(['ID','Etq','X','Y','Ancho','Fmt','lmax','edi','FC','Sobre','ADE','Dlg','Tip','CPAN','Style'])
                enf[-1].append(['DFEC','Desde Fecha','5','20','9','d','10','','','','','','','',''])
                enf[-1].append(['HFEC','Hasta Fecha','105','20','9','d','10','','','','','','','',''])
                enf[-1].append(['PORCEN',']%','65','55','5','2','5','','','','','','','',''])
                p1[-1].append(enf)

                btn=[]
                btn.append(['B1',5,95,90,'ok.gif','Aceptar','a_ACEPTAR','',''])
                btn.append(['B2',105,95,90,'cancel.gif','Cancelar','a_SALIR:n','',''])
                p1[-1].append(['BUTTONS','BID',40,'','',btn])

                lsc.append(p1)
                ## ######################################

                dl = OC.Dialogo(self, titulo='Exportar', campos=lsc,tam=(200,150))
                dl.ShowModal()
                res = dl.res()
                if not res is None:
                    dfec,hfec,porcen = res
                    if dfec==None or hfec==None:
                        Men('Debe indicar el rango de fechas.')
                        return -1
                    cods = select('diario','0',[['0','>=',dfec],['0','<=',hfec]])
                    #
                    resul = []
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
                        fec = Num_aFecha(cod)
                        resul.append([fec,ttsrve,ttsrvj,ttvtse,ttvtsj,ttgas])
                    #
                    hoja = [['Fecha','Servicios','Productos','Gastos']]
                    for ln in resul:
                        fec,ttsrve,ttsrvj,ttvtse,ttvtsj,ttgas = ln
                        ttsrv = ttsrvj + ttsrve*porcen/100.
                        ttvts = ttvtsj + ttvtse*porcen/100.
                        hoja.append([fec,str(ttsrv),str(ttvts),str(ttgas)])
                    #
                    SEP = ','
                    aux = []
                    for ln in hoja:
                        aux.append(SEP.join(ln))
                    hoja= '\n'.join(aux)

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
                    dfec = Num_aFecha(dfec).replace('/','_')
                    hfec = Num_aFecha(hfec).replace('/','_')
                    ruta += '/resumen_'+dfec+'-'+hfec+'.csv'
                    f = open(ruta,"wb")
                    f.write(hoja)
                    f.close()
                    Men('Resumen creado correctamente.')

        except:
            Men(Busca_Error())


        return 0 # No se ejecutó ninguna accion !!!!



#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.PySimpleApp()
    ventana = diario()
    ventana.Show()
    app.MainLoop()