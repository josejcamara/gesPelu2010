#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import wx.calendar
import OC

from OC.Funciones import *

class agenda(OC.Ventana):
    """ Agenda de Citas """

    def __init__(self,padre=None):

        OC.Ventana.__init__(self, padre,'Agenda de Citas',tam=(800,540))
        #
        ls_campos = []

        # Panel para el calendario
        p1 = ['PANEL','P1',530,10,270,250,'','3','',[]]
        enf = ['ENTRYS','ENG','25','50','','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        enf[-1].append(['IDX',':Seleccionado:','120','190','9','d','10','n','','','a_LEE_RG:n','','','',''])
        p1[-1].append(enf)
        #

        p2 = ['PANEL','P2',1,1,525,535,'','','',[]]
        tecnicos = ['MONICA','ELENA','TAMARA']  ##tecnicos = select('tecnicos','TN_DENO') QUE PASA AL BORRAR !!
        cols = []
        for tcn in tecnicos:
            tcn = tcn.split(' ')[0]
            cols.append([tcn,15,'l',0,'','','','','','','','','',''])
        #
        horas = ['9','10','11','12','13','14','15','16','17','18','19','20']
        fracciones = ['00','30']
        filas=[]
        for hora in horas:
            for fraccion in fracciones:
                filas.append(hora+':'+fraccion)
        #
        p2[-1].append(['GRID','AG_CITAS','',2,5,515,20,24,cols,5,filas,''])


        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',550,285,210,225,'','','',[]]
        btn=[]
        btn.append(['B4',55,30,95,'save.png','Grabar','a_GRABA','Grabar Diario',''])
        #btn.append(['B5',5,100,95,'delete.gif','Borrar','a_BORRA','Borrar Diario',''])
        btn.append(['B8',55,170,95,'exit.png','Salir','a_SALIR','',''])
        p3[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(p1)
        ls_campos.append(p2)
        ls_campos.append(p3)

        #
        self._idx = 'IDX'
        self._filedb = 'agenda'
        self._accini='a_ini_var'      # Acción al cargar la ventana
        self._accleer = ''   # Acción despues de leer registro
        self._btfin = ''     # Nombre del boton a ejecutar cuando pulse boton FIN
        #
        self.init_ctrls(ls_campos)
        #
        self.cal = wx.calendar.CalendarCtrl(date=wx.DateTime.Now(),
            parent=self._ct['P1'],pos=wx.Point(5,5),style=wx.calendar.CAL_SHOW_HOLIDAYS|wx.calendar.CAL_MONDAY_FIRST)
        self.cal.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED,self.OnCalSelected)

        self.Ejecuta_Accion(self._accini)

    #
    #-- FUNCIONES DEL CALENDARIO
    #
    def OnCalSelected(self, evt):
        if self.Modifica==1:
            dlg=Men('Ha realizado cambios en la ficha\n¿Desea Continuar sin grabar?','sn','q')
            if dlg=='n': return 0

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
        pb = self

        """ Acciones a ejecutar """
        # Probamos primero si es una accion estandar
        std = OC.Ventana.Ejecuta_Accion(self, accion,obj)
        ok,val = std

        # Comprobar el valor devuelto por si hay que hacer algo
        # Ya se ejecutó la accion. No continuar con la accion normal
        if ok>0:
            return val

        if accion=='a_ini_var':
            pb._ct['IDX'].SetValue(Fecha())
            self.Modifica=0


        return 0 # No se ejecutó ninguna accion !!!!



#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.PySimpleApp()
    ventana = agenda()
    ventana.Show()
    app.MainLoop()
