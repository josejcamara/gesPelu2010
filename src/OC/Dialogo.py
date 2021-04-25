#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx
import Entry
import Grid
import List
import Button
from Funciones import debug
from Funciones import Men
import shelve
import pickle


class Dialogo(wx.Dialog):
    """Clase Dialogo. Es un wx.Dialog modificado para que acepte una lista
    con los campos a introducir en él:
        #-    INSERTAR PANELES:
            ['PANEL',nombre, xini, yini, tamanox, tamanoy,color, CAMPOS_HIJOS]
        #- INSERTAR ENTRADAS:
            ['ENTRY', alto_control, salto_a_-1, style_etiq, style_txt, LS_ENT]
               LS_ENT = [Nombre,etiq,xini,yini,formato,max,ancho,edi,
                               fcal,sobre,ade,dlsel,tip,cpan,style]
    """


    def __init__(self, parent, titulo='', campos=[] , tam=(400,300),btn=True):
        """ Creación de la ventana (Frame) """
        #self._pb=None        # Ventana Padre, será siempre la actual
        self._ct = {}        # Lista de objetos incrustados en la ventana
        self._cta = None     # Objeto Actual que tiene el foco
        self._ctord =[]      # Nombres de los campos editables por orden de foco
        #
        self._parent=parent      # Ventana padre
        self._res = None       # Campo que contiene el codigo del archivo

        tam = (tam[0],tam[1]+23)    # Añadimos el alto de la barra Estado
        wx.Dialog.__init__(self, parent, title=titulo, size = tam)

        self.CenterOnScreen()

        self.init_ctrls(campos)

        if btn:
            okay = wx.Button(self,wx.ID_OK,pos=(100,375))
            okay.SetDefault()
            cancel = wx.Button(self,wx.ID_CANCEL,pos=(200,375))


    #
    #-- Obtener el resultado y destruir el dialogo
    #
    def res(self):
        if self.ShowModal()== wx.ID_OK:
            res=[]
            for campo in self._ctord:
                res.append(self._ct[campo].GetValue())
        else:
            res = None

        self.Close()
        self.Destroy()
        return res

    #
    #
    #
    def SetValue(self,id_campo,valor):
        for campo in self._ct:
            if campo == id_campo:
                self._ct[campo].SetValue(valor)

    #
    #-- INICIALIZACION/INSERCION DE LOS CAMPOS EN LA VENTANA
    #
    def init_ctrls(self, campos, padre=None):
        """ Pinta los campos indicados dentro de la ventana. Formato "campos":
        #-    INSERTAR PANELES:
            ['PANEL',nombre, xini, yini, tamanox, tamanoy,color, CAMPOS_HIJOS]
        #- INSERTAR ENTRADAS:
            ['ENTRY', alto_control, salto_a_-1, style_etiq, style_txt, LS_ENT]
               LS_ENT = [Nombre,etiq,xini,yini,formato,max,ancho,edi,
                               fcal,sobre,ade,dlsel,tip,cpan,style]
        """
        #ultx,ulty = 0,0     # Ultimas posiciones X e Y de un campo
        #sumax,sumay = 0,0   # Distancia a sumar para poner la proxima entrada si -1
        if padre==None: padre= self
        self._ctord = []

        for lnc in campos:
            tipo = lnc[0]

            #- INSERTAR PANELES
            # ['PANEL',nombre, xini, yini, tamanox, tamanoy,color,lista_hijos]
            if tipo=='PANEL':
                self.__Pon_Panel(padre, lnc)


            #- INSERTAR CAMPOS DE TEXTO
            # ['ENTRY', alto_control, salto_a_-1, style_etiq, style_txt, LS_ENT]
            #   LS_ENT = [Nombre,etiq,xini,yini,formato,max,ancho,edi,
            #                   fcal,sobre,ade,dlsel,tip,cpan,style]
            elif tipo=='ENTRYS':
                self.__Pon_Entradas(padre,lnc)


            #- INSERTAR LISTAS
            # ['LIST',nombre, xini, yini, tamanox, tamanoy, cols,
            #        acc_click, acc_dclick]
            elif tipo=='LIST':
                self.__Pon_Lista(padre,lnc)

            #- INSERTAR GRIDS
            elif tipo=='GRID':
                self.__Pon_Grid(padre, lnc)

            #- INSERTAR BOTONES
            elif tipo=='BUTTONS':
                self.__Pon_Botones(padre, lnc)
            #- INSERTAR CHECKBUTTON
            elif tipo=='CHECK':
                self.__Pon_Checks(padre,lnc)

            else:
                debug("Tipo " + str(tipo) + " no definido.")

        self.Refresh()

    #
    #-- Acciones Estandar para las ventanas
    #
    def Ejecuta_Accion(self,accion,obj=None):
        """ Acciones Estandar para las ventanas """

        aux = accion.split(':')
        accion = aux[0]
        arg=[]
        if len(aux)>1: arg = aux[1].split(',')

        if accion=='a_SALIR':
            res = None
            self.Close()
            self.Destroy()
            return (1,'')
        elif accion=='a_ACEPTAR':
            res=[]
            for campo in self._ctord:
                res.append(campo.GetValue())
            self.Close()
            self.Destroy()
        elif accion=='a_pon_cambio':
            pagar = self._ct['PAGAR'].GetValue()
            entrega = self._ct['ENTREGA'].GetValue()
            self._ct['CAMBIO'].SetValue(entrega-pagar)
            return (1,'')

        return (1,'')
        ##return -999

    #
    #-- Pintar un Panel en la ventana
    #
    def __Pon_Panel(self,padre,datos):
        """ Pinta en la Ventana el Panel indicado
        #- datos = datos_panel:
        ['PANEL',Id, xini, yini, tamanox, tamanoy, style, borde,
        Titulo(Si Pestaña)/AccionCambio(Si tabbox), CAMPOS_HIJOS]
        """
        tipo = datos[0]
        if tipo<>'PANEL' and tipo<>'TABBOX':
            return -1

        nombre = datos[1]
        xini,yini = int(datos[2]), int(datos[3])
        tamx,tamy = int(datos[4]), int(datos[5])
        estilo = datos[6]
        #borde = datos[7]
        #acciontb = datos[8]
        hijos = datos[-1]

        posic = wx.Point(xini,yini)
        if tamx==-1: tamx = padre.GetSize()[0]
        if tamy==-1:
            tamy = padre.GetSize()[1]
            if padre==self: tamy = tamy - 30    # Quitamos el tamaño del titulo

        tam = wx.Size(tamx, tamy)
        #-
        elem = wx.Panel(name=nombre, parent=padre, pos=posic, size=tam, style=wx.TAB_TRAVERSAL)
        #-
        # Si hay color de fondo, lo ponemos
        if estilo<>'':
            stl = estilo.split('/')
            for ln in stl:
                if ln[:2]=='B-':
                    rgb = ln[2:].split(':')
                    elem.SetBackgroundColour(wx.Colour(int(rgb[0]), int(rgb[1]), int(rgb[2])))
                else:
                    pass    # Tener en cuenta otros tipos de estilo ???

        #- Ponemos en el diccionario de campos
        if not nombre in self._ct:
            self._ct[nombre]=elem
        else:
            debug('El control '+nombre+' se encuentra repetido.')
        #
        if hijos<>[]:
            self.init_ctrls(hijos,elem)

    #
    #-- Añadir una/varias entradas a la ventana/panel padre
    #
    def __Pon_Entradas(self,padre,datos):
        """ Inserta una/varias entradas en la ventana o panel padre.
          datos:
            ['ENTRYS', Id, alto_control, salto_a_-1, style_etiq,
                style_txt, LS_ENT]

            LS_ENT = [Id,etiq,xini,yini,ancho,formato,lmax,edi,
                               fcal,sobre,ade,dlsel,tip,cpan,style]
        """
        tipo,id,alto,salto,stylelabel,styletext,entradas = datos[:7]
        alto,salto = int(alto),int(salto)
        if tipo<>'ENTRYS':
            return -1

        ultx,ulty = 0,0     # Ultimas posiciones X e Y de un campo
        sumax = 0   # Distancia a sumar para poner la proxima entrada si -1
        for lne in entradas:
            nombre,etiq,xini,yini,ancho,fmt,max = lne[:7]
            edi,fcal,sobre,ade,dlsel,tip,cpan,style = lne[7:15]
            #-
            xini,yini = int(xini),int(yini)
            ancho,max = int(ancho),int(max)

            #-- Asignar Posicion cuando se indica pos -1
            auto = 0
            if xini==-1:
                auto=1
                xini,yini = ultx+sumax, ulty
            elif yini==-1:
                yini = ulty + salto
            elif yini==0:
                yini = ulty

            posic = wx.Point(xini,yini)
            #-- Crear el elemento
            elem = Entry.Entry(self,padre,nombre,posic,etiq,fmt,max,ancho,alto,dlsel)

            #- Comprobamos que no salga fuera de la ventana
            fin = elem.GetPosition()[0] + elem.GetSize()[0]
            xmax = padre.GetSize()[0]
            if fin > xmax and auto:
                xini,yini = 1, ulty + salto
                posic = wx.Point(xini,yini)
                elem.SetPosition(posic)

            # Posicion del ultimo campo
            ultx,ulty = xini, yini
            sumax = elem.GetSize()[0]+10


            #- Editable
            if edi in ['n','i']:
                elem.SetEditable(False)
                elem.Disable()
                if edi=='i': elem.Show(0)
            else:
                self._ctord.append(nombre)

            #- Formula Calculo
            if fcal<>'':
                elem._fcal = fcal
                elem._sobre = sobre

            #- Accion Despues Editar
            if ade<>'':
                elem._ade = ade

            #- Tip de Ayuda
            if tip<>'':
                elem.SetToolTipString(tip)

            #- CPAN
            if cpan<>'':
                elem._cpan = cpan

            #- Estilos
            if styletext<>'':
                stl = styletext.split('/')
                cttext = elem.GetTextCtrl()
                for ln in stl:
                    if ln[:2]=='B-':
                        rgb = ln[2:].split(':')
                        cttext.SetBackgroundColour(wx.Colour(int(rgb[0]), int(rgb[1]), int(rgb[2])))
                    elif ln[:2]=='F-':
                        rgb = ln[2:].split(':')
                        cttext.SetForegroundColour(wx.Colour(int(rgb[0]), int(rgb[1]), int(rgb[2])))
                    else:
                        pass    # Tener en cuenta otros tipos de estilo ???
            if stylelabel<>'':
                stl = stylelabel.split('/')
                ctlabel = elem.GetLabelCtrl()
                for ln in stl:
                    if ln[:2]=='B-':
                        rgb = ln[2:].split(':')
                        ctlabel.SetBackgroundColour(wx.Colour(int(rgb[0]), int(rgb[1]), int(rgb[2])))
                    elif ln[:2]=='F-':
                        rgb = ln[2:].split(':')
                        ctlabel.SetForegroundColour(wx.Colour(int(rgb[0]), int(rgb[1]), int(rgb[2])))
                    else:
                        pass    # Tener en cuenta otros tipos de estilo ???

            # Si hay estilo especifico, lo ponemos
            if style<>'':
                stl = style.split('/')
                cttext = elem.GetTextCtrl()
                for ln in stl:
                    if ln[:2]=='B-':
                        rgb = ln[2:].split(':')
                        cttext.SetBackgroundColour(wx.Colour(int(rgb[0]), int(rgb[1]), int(rgb[2])))
                    elif ln[:2]=='F-':
                        rgb = ln[2:].split(':')
                        cttext.SetForegroundColour(wx.Colour(int(rgb[0]), int(rgb[1]), int(rgb[2])))
                    else:
                        pass    # Tener en cuenta otros tipos de estilo ???

            #- Ponemos en el diccionario de campos
            if not nombre in self._ct:
                self._ct[nombre]=elem
            else:
                Men('El control '+nombre+' se encuentra repetido.')

    #
    #-- Añadir una lista a la ventana/panel padre
    #
    def __Pon_Lista(self,padre,datos):
        """ Añade una lista a la ventana/panel padre
             ['LISTA',id, xini, yini, tamanox, tamanoy, cols,
                anchos_fijos_cols, style, multisel?, borrar?
                acc_click, acc_dclick, acc_borra]
        """
        tipo,nombre,xini,yini,tamx,tamy,cols,wcols,style = datos[:9]
        multisel,borrar,acc,acd,acb=datos[9:14]

        xini,yini = int(xini),int(yini)
        tamx,tamy = int(tamx),int(tamy)

        if tipo<>'LIST':
            return -1

        posic = wx.Point(xini,yini)
        size = (tamx,tamy)
        elem = List.List(self,padre,nombre,posic,size,cols,[],acc,acd)

        #- Ponemos en el diccionario de campos
        self._ctord.append(elem)
        if not nombre in self._ct:
            self._ct[nombre]=elem
        else:
            Men('El control '+nombre+' se encuentra repetido.')

    #
    #-- Poner un Grid en la ventana/panel padre
    #
    def __Pon_Grid(self,padre,datos):
        """ Añade un grid en la ventana/panel padre
            ['GRID',id,titulo,posx,posy,ancho,alto_fila,nfilas,columnas
              ancho_titulo_fila, lista_titus_fila,prop_generales ]

            columnas = [[Titulo, ancho, fmt, lmax, edi, grab, fcal, sobre
                        ade, dlsel, totales, tip, cpan, style]
                        ,
                        ...]
        """
        tipo,nombre,titulo,posx,posy,ancho,hfila,nfilas,cols = datos[:9]
        wfilat,filast,props = datos[9:]

        if tipo<>'GRID':
            return -1

        posx,posy = int(posx),int(posy)
        ancho,hfila=int(ancho),int(hfila)
        nfilas,wfilat = int(nfilas),int(wfilat)

        grid = Grid.Grid(self,padre,nombre,(posx,posy),ancho,hfila,nfilas,cols)

        #- Ponemos en el diccionario de campos
        self._ctord.append(grid)
        if not nombre in self._ct:
            self._ct[nombre]=grid
            self._ctord.append(nombre)
        else:
            Men('El control '+nombre+' se encuentra repetido.')

    #
    #-- Poner uno/varios Botones en la ventana/panel padre
    #
    def __Pon_Botones(self,padre,datos):
        """ Añade uno/varios botones en la ventna/panel padre
        pb,padre,nombre,posic,tamano,imagen,texto,accion,tip)

        """
        tipo,id,alto,style,arco,lsbtn = datos
        alto = int(alto)
        if tipo<>'BUTTONS':
            return -1
        #
        for lnb in lsbtn:
            nombre,posx,posy,ancho,imagen,texto,accion,tip = lnb[:8]
            ancho = int(ancho)
            posic = (int(posx),int(posy))
            btn = Button.Button(self,padre,nombre,posic,(ancho,alto),imagen,texto,accion,tip)
            if style<>'': btn.SetStyleText(style)
            #if stylebutton<>'': btn.SetStyleButton(stylebutton)

        #
    #-- Poner un CheckBox en la ventana/panel padre
    #
    def __Pon_Checks(self,padre,datos):
        """ Añade un check en la ventana/panel padre
        """
        tipo,id,posx,posy,alto,ancho,texto,valor,accion,tip,style = datos
        if tipo<>'CHECK':
            return -1

        alto,ancho = int(alto), int(ancho)
        posic = (int(posx),int(posy))
        tam = (ancho,alto)
        #
        elem = Button.CheckButton(self,padre,id,posic,tam,texto,accion)
        ##if tip<>'': ....
        ##if style<>'': ...

        #- Ponemos en el diccionario de campos
        self._ctord.append(id)
        if not id in self._ct:
            self._ct[id]=elem
        else:
            Men('El control '+id+' se encuentra repetido.')

    #
    #-- Moverse al siguiente campo de la ventana
    #
    def Next_Ctrl(self,actual):
        lsct = self._ctord
        tab=-1
        if actual._name in lsct:
            tab = lsct.index(actual._name)
        if tab<len(lsct)-1:
            # Si tipo==Entry: SetFocus, Si tipo==Grid: SetCellCursor
            self._ct[lsct[tab+1]].SetFocus()
    #
    #-- Moverse al siguiente campo de la ventana
    #
    def Prev_Ctrl(self,actual):
        lsct = self._ctord
        tab=-1
        if actual._name in lsct:
            tab = lsct.index(actual._name)
        if tab>0:
            # Si tipo==Entry: SetFocus, Si tipo==Grid: SetCellCursor
            self._ct[lsct[tab-1]].SetFocus()


#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    debug('main')###
    ls_campos=[]
    #
    p1 = ['PANEL','P1',0,0,-1,-1,'B-236:44:26/RF','','',[]]
    hijosp1=[]
    hijosp1.append(['E1','Código',10,15,6,'%',7,'','','','','ar_ls','codigo del cliente','clientes',''])
    hijosp1.append(['E2','Nombre',-1,15,6,'l',10,'','','','','','','',''])
    p1[-1].append(['ENTRYS','EX',22,50,'F-255:255:0','B-0:0:0/F-255:255:255',hijosp1])


    # PANELES: ['PANEL',nombre, xini, yini, tamanox, tamanoy,color,lista_hijos]
    ls_campos.append(p1)

    app = wx.App(False)
    ventana = Dialogo(None)
    ventana.init_ctrls(ls_campos)

    ventana.Show()
    app.MainLoop()
