#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx,os
import OC

from OC.Funciones import *

class Manage_Form(OC.Ventana):
    """ Edicion de Informes """

    def __init__(self,filePath):
        #
        self.filePath = filePath
        self.fileName = os.path.join(filePath,'forms')
        #
        OC.Ventana.__init__(self, None,'Edición de Informes',tam=(800,600))
        #
        ls_campos = []

        # Panel Busqueda Informe
        p1 = ['PANEL','P1',1,1,200,350,'','3','',[]]
        enf = ['ENTRYS','ENG','25','50','','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        ##enf[-1].append(['FILE','Archivo','10','15','12','l','20','','','','a_lista_inf','','Fichero al que pertenece','',''])
        ##p1[-1].append(enf)
        #
        cols=[['Informe','l']]
        ls = ['LIST','LINF','10','50','150','250',cols,'','','','','a_carga_inf','','']
        p1[-1].append(ls)
        #

        # Panel Definicion Informe
        p2 = ['PANEL','P2',201,1,600,550,'','3','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        enf = ['ENTRYS','ENG','25','50','','',[]]
        enf[-1].append(['DESCRIP','Descripcion','10','15','35','l','50','','','','','','','',''])
        enf[-1].append(['ANTES','Accion Antes','10','60','18','l','50','','','','','','','',''])
        enf[-1].append(['ACCION','Accion Relleno','-1','','18','l','50','','','','','','','',''])
        enf[-1].append(['DESPUES','Accion Despues','-1','','18','l','50','','','','','','','',''])
        p2[-1].append(enf)

        # GRID CAMPOS DEL INFORME
        cols = []
        cols.append(['Campo',7,'l',0,'','','','','','','','','',''])
        cols.append(['Titulo',20,'l',0,'','','','','','','','','',''])
        cols.append(['Fmt',4,'l',1,'','','','','','','','','',''])
        cols.append(['Ancho',5,'i',0,'','','','','','','','','',''])
        cols.append(['Tot?',4,'l',1,'','','','','','','','','',''])
        gridc =['GRID','GRIDC','Columnas del Informe',5,120,590,22,8,cols,0,'','']

        # GRID DE PREGUNTAS DEL INFORME
        cols = []
        cols.append(['Campo',7,'l',0,'','','','','','','','','',''])
        cols.append(['Titulo',20,'l',0,'','','','','','','','','',''])
        cols.append(['Fmt',4,'l',1,'','','','','','','','','',''])
        cols.append(['Lmax',5,'i',0,'','','','','','','','','',''])
        cols.append(['Op',4,'l',2,'','','','','','','','','',''])
        gridp =['GRID','GRIDP','Preguntas del Informe',5,360,590,22,6,cols,0,'','']
        #
        p2[-1].append(gridc)
        p2[-1].append(gridp)

        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',1,350,200,200,'','3','',[]]
        btn=[]
        btn.append(['B1',3,10,95,'new.png','Nuevo','a_nuevo','Crear Informe',''])
        btn.append(['B31',3,65,95,'save.png','Grabar','a_graba','Grabar Informe',''])
        btn.append(['B4',100,65,95,'delete.png','Borrar','a_borra','Borrar Informe',''])
        btn.append(['B5',35,120,95,'exit.png','Salir','a_SALIR','Salir',''])
        p3[-1].append(['BUTTONS','BID',50,'','',btn])

        ls_campos.append(p1)
        ls_campos.append(p2)
        ls_campos.append(p3)

        #
        self._idx = ''
        self._filedb = ''
        self._accini='a_ini_var'      # Acción al cargar la ventana
        self._accleer = ''   # Acción despues de leer registro
        self._btfin = ''     # Nombre del boton a ejecutar cuando pulse boton FIN
        #
        self.init_ctrls(ls_campos)
        #
        self.Ejecuta_Accion(self._accini)

    #
    #- Acci�n al cambiar seleccionado de la lista de archivos
    #
    def onChangeFile(self,event):
        self.Ejecuta_Accion('a_lista_inf')

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
            tablas = bsddb.btopen(os.path.join(self.filePath,'dicc'))
            lista_files = tablas.keys()
            tablas.close()
            lista_files.insert(0,'')
            wx.StaticText(self._ct['P1'],-1,"Archivo:",(10,5))
            sele = wx.Choice(self._ct['P1'],-1,(10,20),(150,25),choices=lista_files)
            sele.Bind(wx.EVT_CHOICE, self.onChangeFile)
            self._FILE = sele

        #
        #-- Rellenar la lista de informes de un fichero
        #
        elif accion=='a_lista_inf':
            items = self._FILE.GetItems()
            sele = self._FILE.GetSelection()
            tabla = items[sele].encode('latin-1')
            #
            datos_inf = lee_dicc(self.fileName,tabla)
            if datos_inf==None: datos_inf={}
            #
            ls_inf = datos_inf.keys()
            linf=[]
            for inf in ls_inf:
                linf.append([inf])
            self._ct['LINF'].SetValue(linf)
            self._ct['DESCRIP'].SetValue('')
            self._ct['ANTES'].SetValue('')
            self._ct['ACCION'].SetValue('')
            self._ct['DESPUES'].SetValue('')
            self._ct['GRIDC'].SetValue([])
            self._ct['GRIDP'].SetValue([])
        #
        #-- Cargar los datos de un informe
        #
        elif accion=='a_carga_inf':
            items = self._FILE.GetItems()
            sele = self._FILE.GetSelection()
            tabla = items[sele].encode('latin-1')
            inf = self._ct['LINF'].GetValue()
            #
            ls_inf = lee_dicc(self.fileName,tabla)
            #
            if not inf in ls_inf.keys():
                # Le ha dado a informe nuevo y se ha seleccionado
                deno,antes,accion,despues,gridc,gridp='','','','',[],[]
            else:
                deno,antes,accion,despues,gridc,gridp = ls_inf[inf]
            self._ct['DESCRIP'].SetValue(deno)
            self._ct['ANTES'].SetValue(antes)
            self._ct['ACCION'].SetValue(accion)
            self._ct['DESPUES'].SetValue(despues)
            self._ct['GRIDC'].SetValue(gridc)
            self._ct['GRIDP'].SetValue(gridp)
            Foco(self,'DESCRIP')

        #
        #-- Crear un nuevo informe
        #
        elif accion=='a_nuevo':
            items = self._FILE.GetItems()
            sele = self._FILE.GetSelection()
            tabla = items[sele]
            if tabla=='':
                Men('Debe rellenar el fichero al que pertenece el informe')
                return 1
            id = Entra_dlg(self,titu='Nuevo Informe '+tabla,text='Id Informe '+tabla,value='')
            if id==None: return 1
            lsinf = self._ct['LINF'].GetValue(fmt='L')
            if id in lsinf:
                Men('Ya existe un informe con ese id')
                return 1
            lsinf.append([id])
            self._ct['LINF'].SetValue(lsinf)
            self._ct['LINF'].Sel_Item(len(lsinf)-1) # último
            self._ct['DESCRIP'].SetValue('')
            self._ct['ANTES'].SetValue('')
            self._ct['ACCION'].SetValue('')
            self._ct['DESPUES'].SetValue('')
            self._ct['GRIDC'].SetValue([])
            self._ct['GRIDP'].SetValue([])

        #
        #-- Grabar un informe
        #
        elif accion=='a_graba':
            ls_inf = self._FILE.GetItems()
            selinf = self._FILE.GetSelection()
            tabla = ls_inf[selinf].encode('latin-1')
            info = self._ct['LINF'].GetValue()
            #
            if tabla=='' or info==None:
                Men('No tiene seleccionado ningún informe.')
                return -1
            #
            deno = self._ct['DESCRIP'].GetValue()
            antes = self._ct['ANTES'].GetValue()
            accion = self._ct['ACCION'].GetValue()
            despues = self._ct['DESPUES'].GetValue()
            gridc = self._ct['GRIDC'].GetValue()
            gridp = self._ct['GRIDP'].GetValue()
            #
            datos = [deno,antes,accion,despues,gridc,gridp]
            #
            ls_inf = lee_dicc(self.fileName,tabla)
            if ls_inf==None: ls_inf={}
            #
            if info in ls_inf.keys():
                dl = Men('Ya existe el informe '+info+'.\n¿Desea Sobreescribir?','sn')
                if dl=='n': return -1
            ls_inf[info]=datos
            #
            ok = graba_dicc(self.fileName,tabla,ls_inf)
            if ok<>None:
                Men('Listado Guardado',img='i')
                self.Ejecuta_Accion('a_carga_dicc')

        #
        #-- Borrar un informe
        #
        elif accion=='a_borra':
            ls_inf = self._FILE.GetItems()
            selinf = self._FILE.GetSelection()
            tabla = ls_inf[selinf].encode('latin-1')
            info = self._ct['LINF'].GetValue()
            #
            if tabla=='' or info==None:
                Men('No tiene seleccionado ningún informe para borrar')
                return -1
            #
            dl = Men('¿Está seguro de borrar el listado '+info+'?','sN')
            if dl=='n': return -1
            #
            ls_inf = lee_dicc(self.fileName,tabla)
            if ls_inf==None: ls_inf={}
            #
            if info in ls_inf.keys():
                del ls_inf[info]
            #
            ok = graba_dicc(self.fileName,tabla,ls_inf)
            Men('Listado Borrado',img='i')
            self.Ejecuta_Accion('a_lista_inf')

        return 0 # No se ejecutó ninguna accion !!!!



#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App(False)
    ventana = Manage_Form()
    ventana.Show()
    app.MainLoop()