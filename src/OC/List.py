#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
from Funciones import *

class List():

    def __init__(self,pb,padre,nombre,posic,size=(-1,-1),cols=[],anchos=[],onclick="",ondclick=""):
        """ Creaci�n de la lista:
          pb -> Padre Base. Ventana que contiene el codigo de las acciones
          padre -> Ventana/Panel padre del objeto
          nombre -> Nombre del campo
          posic -> Posici�n de la lista dentro del padre (posx,posy) o wx.Point
          size -> (tamx,tamy). Pareja de enteros indicando tama�o
          cols -> Lista de columnas de la lista ([[col1,fmt1],[col2,fmt2],...]
          anchos -> Anchos de las columnas, en caso de asignar fijos
          onclick -> Acci�n a Ejecutar al seleccionar una fila
          ondclick -> Acci�n a Ejecutar al doble-click sobre fila
        """
        lis = wx.ListCtrl(name=nombre, parent=padre, pos=posic, style=wx.LC_REPORT)

        #- Ponemos las columnas si se han definido
        fmtlis=[]
        i=0
        for col in cols:
            ncol,fmt = col
            #- A�adimos la columna
            ncol = ncol.decode('latin-1')
            lis.InsertColumn(i,ncol)
            fmtlis.append(str(fmt))
            ##- Definimos el ancho de la columna
            ancho = wx.LIST_AUTOSIZE_USEHEADER
            if i<len(anchos): ancho=anchos[i]
            lis.SetColumnWidth(i,ancho)
            ##lis.SetColumnWidth(i,wx.LIST_AUTOSIZE);
            #
            i+=1
        #
        lis.SetPosition(posic)
        #if size<>(-1,-1):
        #    lis.Size = wx.Size(size[0],size[1])
        #
        sizex, sizey = size
        if sizex==-1: sizex = padre.GetSize()[0]
        if sizey==-1: sizey = padre.GetSize()[1]
        lis.Size = wx.Size(sizex,sizey)
        #
        lis.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onClick)
        ##lis.Bind(wx.EVT_LEFT_DCLICK,self.onDclick)
        lis.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onDclick)
        #
        self._name = nombre         # Nombre del Control
        self._pb = pb               # Ventana Padre (Contiene Acciones click)
        self.__ctlis = lis          # Control ListCtrl
        self.__anchos = anchos      # Anchos de las columnas de la lista
        self.__fmtlis = fmtlis       # Formato de cada una de las columnas
        self.__data = []            # Datos de la lista
        self._onclick = onclick     # Accion al hacer click sobre un elemento
        self._ondclick = ondclick   # Acci�n al doble click sobre un elemento

    def GetListCtrl(self):
        """ Devuelve el control wx.ListCtrl que forma el objeto """
        return self.__ctlis

    def GetValue(self,fmt=''):
        """ Devuelve el valor seleccionado en la lista:
            fmt = '' -> Valor de la primera columna en la fila seleccionada
            fmt = 'l' -> Lista con los valores de toda la fila
            fmt = 'L' -> Lista Bidimensional con los valores de toda la lista.
         """
        index = self.__ctlis.GetFirstSelected()

        value = None
        objlis = self.__ctlis
        fmtlis = self.__fmtlis
        if fmt=='':
            if index==-1: return None
            value = self.__ctlis.GetItem(index).GetText()
            value = value.encode('latin-1')

        elif fmt=='l':
            if index==-1: return None
            value = self.__data[index]

        elif fmt=='L':
            value = self.__data


        return value

    def SetValue(self,data,acc='s'):
        """ Asigna a la lista los valores seleccionados """
        lis = self.__ctlis
        fmtlis = self.__fmtlis
        self.__data = data
        lis.DeleteAllItems()

        for lnd in data:
            if isinstance(lnd,str): lnd=[lnd]
            nfila = lis.InsertItem(sys.maxint,lnd[0])
            ncol=0
            for fmt in fmtlis:
                try:
                    valor = lnd[ncol]
                except:
                    valor = ''
                #
                if fmt == 'd':
                    valor = Num_aFecha(valor)
                elif fmt =='i':
                    valor = str(valor)
                elif fmt in ('0','1','2','3','4','5','6','7','8','9'):
                    try:
                        valor = str(round(valor,int(fmt)))
                    except:
                        valor = '0.0'
                else:
                    valor =str(valor)   # No deber�a llegar, pero por si...
                #
                valor = valor.decode('latin-1')
                lis.SetItem(nfila,ncol,valor)
                #
                ncol += 1
        #-
        #- Reasignamos el ancho de la columna
        anchos = self.__anchos
        if anchos==[]:
            anchos = [0]*len(self.__fmtlis)
            for i in range(lis.GetColumnCount()):
                col = lis.GetColumn(i)
                anchos[i] = len(col.Text)

            if data<>[]:    # Ajustamos al ancho maximo de todas las filas
                for fdata in data:
                    if isinstance(fdata,str): fdata=[fdata]
                    i=0
                    for cdata in fdata:
                        if i>=len(fmtlis): continue
                        if fmtlis[i]=='d':  # Fechas siempre mismo ancho
                            anchos[i]=10
                            continue
                        if isinstance(cdata,float) or isinstance(cdata,int):
                            cdata=str(cdata)
                        if len(cdata) > anchos[i]: anchos[i] = len(cdata)
                        i+=1
        #
        for i in range(len(anchos)):
            tam = anchos[i]*10
            lis.SetColumnWidth(i,tam)
            ##lis.SetColumnWidth(i,wx.LIST_AUTOSIZE);

    def Sel_Item(self,pos=-1,text=''):
        """Selecciona una fila de la lista, indicada por texto o posicion"""
        if pos>=0:
            self.__ctlis.Select(pos,True)
        else:
            todos = self.GetValue(fmt='l')
            if todos==None: return
            if text in todos:
                pos = todos.index(text)
                self.__ctlis.Select(pos,True)

    def SelAll(self):
        """ Selecciona todos los elementos de la lista """
        pass

    def DselAll(self):
        """ Deselecciona todos los elementos de la lista """
        pass

    def SetAnchos(self,anchos):
        self.__anchos = anchos
        lis = self.__ctlis
        for i in range(lis.GetColumnCount()):
            ancho = wx.LIST_AUTOSIZE
            if i<len(anchos): ancho=anchos[i]
            lis.SetColumnWidth(i,ancho)

    def GetAnchos(self):
        return self.__anchos

    #-------
    def onClick(self,event):
        """ Acci�n al Seleccionar un elemento de la lista """
        pb = self._pb
        if pb==None:
            value = self.GetValue()
        elif self._onclick<>'':
            pb.Ejecuta_Accion(self._onclick)
        event.Skip()

    def onDclick(self,event):
        """ Ejecutar la acci�n al hacer doble click sobre la lista """
        pb = self._pb
        if pb==None:
            value = self.GetValue()
        elif self._ondclick<>'':
            pb.Ejecuta_Accion(self._ondclick)
        event.Skip()

"""
COMBO-BOX

"""
class Combo():
    def __init__(self,pb,padre,nombre,posic,size=(-1,-1),choices=[],onchange=""):

        label = wx.StaticText(padre,-1,"Seleccione",posic)
        lis = Choice(padre,nombre,posic,size,choices)


if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = wx.Frame(None,title="Prueba de la Clase List")
    frame.SetSize((800,600))
    frame.CentreOnScreen()
    #
    p1 = wx.Panel(name='P1', parent=frame)
    #
    cols = [['Codigo','l'],['Fecha','d'],['Entero','i'],['Decimal2','2']]
    l1 = List(None,p1,'L1',(100,100),(300,200),cols=cols)
    value=[]
    value.append(['00000',Fecha(),10,23])
    value.append(['00000',Sm_Fecha(Fecha(),1),5,13.23333])
    l1.SetValue(value)
    #
    frame.Show()
    app.MainLoop()
