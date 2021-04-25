#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx
import wx.adv
import wx.lib.calendar
import OC

from OC.Funciones import *

class caja_dia(OC.Ventana):
    """ Cuadrante Caja Diaria """

    def __init__(self,padre=None):

        OC.Ventana.__init__(self, padre,'Cuadrante Caja',tam=(600,255))
        #
        ls_campos = []

        # Panel para el calendario
        p1 = ['PANEL','P1',1,1,300,250,'','1','',[]]
        enf = ['ENTRYS','ENG','25','50','','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        enf[-1].append(['IDX',':Seleccionado:','120','190','9','d','10','n','','','a_LEE_RG:n','','','',''])
        p1[-1].append(enf)
        #

        p2 = ['PANEL','P2',301,1,300,250,'','','',[]]
        eng = ['ENTRYS','ENG','25','50','','',[]]
        #eng[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        eng[-1].append(['CJ_INI',':Caja Inicial','100','10','10','2','10','','','','','','','',''])
        eng[-1].append(['CJ_VTAS',': Ventas Hoy','100','40','10','2','10','','','','','','','',''])
        eng[-1].append(['CJ_GAS',': Gastos Hoy','100','70','10','2','10','','','','','','','',''])
        eng[-1].append(['CJ_CIE', ':Cierre Caja','100','100','10','2','10','','','','','','','',''])
        eng[-1].append(['CJ_DES', ':  Descuadre','100','130','10','2','10','','','','','','','',''])
        p2[-1].append(eng)

        btn=[]
        btn.append(['B3',220,60,50,'refresh.png','','a_actualiza','Recalcular Importes Hoy',''])
        btn.append(['B4',30,170,95,'save.png','Grabar','a_GRABA','',''])
        btn.append(['B8',160,170,95,'exit.png','Salir','a_SALIR','',''])
        p2[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(p1)
        ls_campos.append(p2)

        #
        self._idx = 'IDX'
        self._filedb = 'caja_dia'
        self._accini='a_ini_var'      # Acción al cargar la ventana
        self._accleer = ''   # Acción despues de leer registro
        self._btfin = ''     # Nombre del boton a ejecutar cuando pulse boton FIN
        #
        self.init_ctrls(ls_campos)
        #
        self.cal = wx.adv.CalendarCtrl(
            date=wx.DateTime.Now(),
            parent=self._ct['P1'],
            pos=wx.Point(5,5),
            style=wx.adv.CAL_MONDAY_FIRST
            )
        self.cal.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,self.OnCalSelected)

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
        self.Modifica=0

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
            
        elif accion=='a_actualiza':
            fec = pb._ct['IDX'].GetValue()
            #
            ttini = pb._ct['CJ_INI'].GetValue()
            ttfin = pb._ct['CJ_CIE'].GetValue()
            #
## ANTES DE CREAR EL FICHERO DE COBROS....            
##            ventas = select('alb-venta','0',[['AV_FEC','=',fec]])
##            ttvtas=0
##            for cod in ventas:
##                rg = lee('alb-venta',cod)
##                if rg==1: continue
##                if rg['AV_PTJ']==1:continue #Pago tarjeta, no influye saldo
##                ttvtas+= rg['AV_TTT']
            cobros = select('cobros','0',[['CB_FEC','=',fec]])
            ttvtas=0
            for cod in cobros:
                rg = lee('cobros',cod)
                if rg==1: continue
                if rg['CB_TARJ']==1: continue   #Pago tarjeta, no influye saldo
                ttvtas += rg['CB_IMPO']
            pb._ct['CJ_VTAS'].SetValue(ttvtas)
            #
            gastos = select('gastos','0',[['GA_FEC','=',fec]])
            ttgas=0
            for cod in gastos:
                rg=lee('gastos',cod)
                if rg==1: continue
                ttgas += rg['GA_IMPO']
            pb._ct['CJ_GAS'].SetValue(ttgas)
            #
            resto = ttini + ttvtas - ttgas
            descuadre = ttfin - resto
            pb._ct['CJ_DES'].SetValue(descuadre)
            #
            Men('Datos Actualizados')

        return 0 # No se ejecutó ninguna accion !!!!



#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App(False)
    ventana = caja_dia()
    ventana.Show()
    app.MainLoop()

# import wx
# import wx.adv
# class MyCalendar(wx.Frame):

#     def __init__(self, *args, **kargs):
#         wx.Frame.__init__(self, *args, **kargs)
#         self.cal = wx.adv.CalendarCtrl(self, 10, wx.DateTime.Now())
#         self.cal.Bind(wx.adv.EVT_CALENDAR, self.OnDate)

#     def OnDate(self,event):
#         print(self.cal.GetDate())


# if __name__ == '__main__':
#     app = wx.App()
#     frame = MyCalendar(None)
#     frame.Show()
#     app.MainLoop()