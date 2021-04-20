#!/usr/bin/env python
# -*- coding: utf-8 -*-

import OC
from OC.Funciones import *

import shutil
import os
import os.path
import datetime

class Inicio(OC.Ventana):
    """ Ficha para manejar los archivos de la base de dato """

    def __init__(self,padre=None):
        OC.Ventana.__init__(self, padre,'Inicio',tam=(490,250))

        ls_campos = []
        #
        p1 = ['PANEL','P1',0,0,500,300,'',[]]
        #---
        hp1=[]  # hijos de P1
        #
        btn=[]
        btn.append(['B1',10,10,110,'people.png','Clientes','a_CPAN:clientes','Ficha de Clientes'])
        btn.append(['B2',130,10,110,'proveedor.png','Proveedor','a_CPAN:proveedores','Proveedores'])
        btn.append(['B3',250,10,110,'articulos.png','Articulos','a_CPAN:articulos','Artículos'])
        btn.append(['B4',370,10,110,'persons.png','Tecnicos','a_CPAN:tecnicos','Tecnicos'])
        btn.append(['B5',10,65,110,'calendar.png','Agenda','a_CPAN:agenda','Agenda'])
        #btn.append(['B6',130,120,110,'book.png','Diario','a_CPAN:diario','Diario de Ingresos y Gastos'])
        btn.append(['B7',250,65,110,'tpv.png','TPV','a_CPAN:tpv','TPV Ventas'])
        btn.append(['B8',370,65,110,'gastos.png','Gastos','a_CPAN:gastos','Gastos'])
        btn.append(['B9',10,120,110,'caja.png','Cierre\nCaja','a_CPAN:caja_dia','Caja Diaria'])
        btn.append(['B10',130,65,110,'page.png','Resumen\nSituacion','a_CPAN:resumen_m',''])
        btn.append(['B12',250,120,110,'plus.png','Copia\nSeguridad','a_copia_seg','Hacer Copia Seguridad'])
        btn.append(['B8',370,120,110,'cobros.png','Cobros','a_CPAN:cobros','Cobros'])
        #btn.append(['B5',325,10,100,'config.png','Config','a_CPAN:parametros','Parametros de Configuraci�n'])
        btn.append(['B10',130,120,110,'tools.png','Borra\n2010','a_borra_2010',''])
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

        """ Acciones a ejecutar """
        # Probamos primero si es una accion estandar
        std = OC.Ventana.Ejecuta_Accion(self, accion,obj)
        ok,val = std

        # Comprobar el valor devuelto por si hay que hacer algo
        # Ya se ejecutó la accion. No continuar con la accion normal
        if ok>0:
            return val

        if accion=='a_copia_seg':
            from global_var import DIR_DATA
            #
            dir_apl = os.getcwd()
            hoy = datetime.date.today()
            anio,mes,dia = str(hoy.year),str(hoy.month).zfill(2),str(hoy.day).zfill(2)

            origen = DIR_DATA   #os.path.join(dir_apl,'data')
            #
            destino = os.path.join(os.environ['HOME'],'Dropbox')
            destino = os.path.join(destino,'gesPelu')
            destino = os.path.join(destino,anio+'_'+mes+'_'+dia)

            if os.path.isdir(destino): shutil.rmtree(destino)  # Si existe, lo borramos

            shutil.copytree(origen,destino)

            Men('Copia de datos realizada en '+destino)
            
        elif accion=='a_borra_2010':
            dlg = Men('¿Está seguro de borrar registros?','sn','q')
            if dlg=='n': return 
            #
            dlp = wx.ProgressDialog ('Buscando', 'Buscando', maximum = 2 )
            dlp.Update (1, 'Seleccionando...' )
            #
            resul = select('alb-venta','0',[['AV_FEC','<',Fecha_aNum('01/01/2011')]])
            dlp.Close()
            dlp.Destroy()
            #
            ttt = len(resul)+1
            dlp = wx.ProgressDialog ('Borrando', 'Borrando', maximum = ttt )
            #-
            from global_var import DIR_DATA
            ruta_datos = DIR_DATA +'/alb-venta.db'
            f = bsddb.btopen(ruta_datos)
            #print f.keys()[:100]
            #
            x=0
            for idx in resul:
                x+=1
                dlp.Update (x, str(x) + '/' + str(ttt) )
                #wx.Sleep(0.25)
                f[idx]=''
                del f[idx]
            dlp.Close()
            dlp.Destroy()
            #
            f.close()


            Men('Registros Borrados.',img='i')


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = Inicio()
    return win

#----------------------------------------------------------------------

#############################################################
#
#
##############################################################
if __name__ == "__main__":
    import wx
    import global_var

    app = wx.App(False)

    ventana = Inicio()
    app.MainLoop()
