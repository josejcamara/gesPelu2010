#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx
import wx.lib.buttons as buttons
from Funciones import *
# from Ventana import *
import string
import os

try:
    from global_var import DIR_IMG
except:
    DIR_IMG = '../../img'



#- MIRAR ESTO COMO OTRO TIPO DE ENTRADA PARA CUANDO TIENE LISTA
#sampleList=['Cero','Uno','Dos','Tres']
#wx.ComboBox(self,-1,"valor",(15,30),wx.DefaultSize,sampleList,wx.CB_SIMPLE)
#wx.Choice(self,-1,"value",posic,size,sampleList,style)


class Entry():
    """ Entrada de texto, con su etiqueta y propiedades adicionales
    _name = ""      # Nombre de la entrada
    _vant = ""      # Valor anterior del campo
    _fmt = "l"      # Formato de la entrada de texto (l,%,i,d,p,mX,0,1,2,3,...)
    _lmax = 0       # Longitud máxima del campo
    _pb = None      # Padre base. Será la ventana que contine el codigo de las acciones
    _fcal = ""      # Nombre de la acción a ejecutar cuando se entre en el campo
    _sobre= ""      # si "s", sobreescribir valor cuando de ejecuta la formula calculo
    _ade = ""       # Acción a ejecutar despues de editar (salir foco) la entrada
    _dlsel = ""     # Dialogo de selección para el campo
    _cpan=""        # Nombre de la ventana a abrir al pulsar F4 sobre el campo
    __ctlabel=None   # Campo etiqueta de texto
    __cttext =None   # campos texto
    __btnsel = None # Botón de seleccion, en caso de que haya
    _adk = ""       # Acción al pulsar una tecla valida """


    #
    #--- Inicialización
    #
    def __init__(self,pb,padre,nombre,posic=(-100,-100),etiq='',fmt='l',lmax=0,ancho=10,alto=22,dlsel=''):
        """
        #
        #-- Inicializacion del Campo de Entrada
        #    pb = Padre Base. Ventana que contiene todos los paneles y codigo de acciones
        #    padre = Padre (Panel, ventana...)
        #    posic = wx.Point(int,int) Posiciones x e y en el padre
        #    etiq = (string) Etiqueta a poner al campo (:etiq la pone a la izq)
        #    fmt = (string) Formato de la entrada ( l=Texto, %=TextoAjustado, d=Fecha,
        #                   i=Entero, 0,1,2..=Flotante con n decimales, p = password
        #                   mx = Multilinea con x lineas visibles
        #    lmax = (int) Longitud maxima del texto introducido
        #    ancho = ancho del campo de texto
        #    alto = alto del campo de texto
        #    dlsel = dialogo de selección
        """
        if len(posic)==2:
            posic = wx.Point(posic[0],posic[1])
        #-
        xsize = wx.Size(ancho*10,alto)
        if fmt=='p' or fmt=='P':
            text = wx.TextCtrl(name=nombre, parent=padre, style=wx.TE_PASSWORD)
        elif fmt.startswith('m') or fmt.startswith('M'):
            alto = alto*(int(fmt[1:]))
            xsize = wx.Size(ancho*10,alto)
            text = wx.TextCtrl(name=nombre, parent=padre, style=wx.TE_MULTILINE)
        else:
            text = wx.TextCtrl(name=nombre, parent=padre)
        #
        text.SetPosition(posic)
        text.SetSize(xsize)
        self._name = nombre         # Nombre de la entrada
        self._vant = ''             # Valor anterior del campo
        self._fmt = fmt             # Formato de la entrada de texto (l,%,i,d,p,mX,0,1,2,3,...)
        self._lmax = lmax           # Longitud máxima del campo
        self._pb = pb               # Padre base. Será la ventana que contine el codigo de las acciones
        self._fcal=""               # Nombre de la acción a ejecutar cuando se entre en el campo
        self._sobre=""              # si "s", sobreescribir valor cuando de ejecuta la formula calculo
        self._ade=""                # Accion despues de editar
        self._adk=""                # Accion al pulsar tecla
        self._dlsel = dlsel         # Dialogo de selección para el campo
        self._cpan = ""             # Nombre de la ventana a abrir al pulsar F4 sobre el campo

        #
        if lmax>0 and not text.IsMultiLine(): text.SetMaxLength(lmax)


        #- Posicionamiento de la etiqueta
        if etiq[:1]==':' or etiq[:1]=='[':   # Poner etiqueta a la izquierda del texto
            etiq=etiq[1:]
            label = wx.StaticText(padre,label=etiq)
            text.SetPosition(posic)
            label.SetPosition((posic.x - label.GetSize()[0],posic.y+2))
        elif etiq[:1]==']':     # Poner la etiqueta a la derecha del texto
            etiq=etiq[1:]
            label = wx.StaticText(padre,label=etiq)
            label.SetPosition((posic.x + text.GetSize()[0]+10,posic.y+5))
        else:   # Poner la etiqueta encima del texto
            label = wx.StaticText(padre,label=etiq)
            label.SetPosition((posic.x,posic.y-15))

        self.__ctlabel = label
        self.__cttext = text
        self.__btnsel = None    # Boton de seleccion

        # Asociar EVENTOS
        text.Bind(wx.EVT_KEY_DOWN, self.Al_Pulsar_Tecla)
        text.Bind(wx.EVT_KEY_UP, self.Al_Soltar_Tecla)
        text.Bind(wx.EVT_SET_FOCUS, self.Al_Entrar)
        text.Bind(wx.EVT_KILL_FOCUS, self.Al_Salir)
        #self.Bind(wx.EVT_SET_CURSOR, self.Prueba)    ## Al pasar el ratón por encima!!
        #if button<>None: button.Bind(wx.EVT_BUTTON, self.Al_Pulsar_Boton)
        #text.Bind(wx.EVT_TEXT_ENTER,self.Prueba)
        #text.Bind(wx.EVT_TOOL_ENTER,self.Prueba)

    #
    #
    #
    def Get_ADE(self):
        return self._ade
    #
    #
    #
    def Set_ADE(self,ade):
        self._ade = ade

    #
    #
    #
    def Set_ADK(self,adk):
        self._adk = adk

    #
    #
    #
    def SetFmt(self,fmt):
        self._fmt = fmt

    #
    #
    #
    def GetFmt(self):
        return self._fmt

    #
    #-- Devuelve el campo TextCtrl que forma el objeto Entry
    #
    def GetTextCtrl(self):
        """ Devuelve el campo TextCtrl que forma el objeto Entry """
        return self.__cttext

    #
    #-- Devuelve el staticText que forma el objeto Entry
    #
    def GetLabelCtrl(self):
        """ Devuelve el staticText que forma el objeto Entry """
        return self.__ctlabel
    #
    #
    #
    def GetSeleButton(self):
        """ Devuelve el botón de selección """
        return self.__btnsel

    #
    #-- Poner en una posición concreta
    #
    def SetPosition(self,posic):
        """ Pone el elemento en la posicion indicada (Etiqueta y entrada texto)
            'posic' puede ser una lista con los elementos (posx,posy)
            o un objeto wx.Point
        """
        self.__cttext.SetPosition(posic)

        label = self.__ctlabel
        etiq = label.GetLabel()
        text = self.__cttext
        if etiq[:1]==':' or etiq[:1]=='[':   # Poner etiqueta a la izquierda del texto
            etiq=etiq[1:]
            label.SetPosition(posic)
            text.SetPosition((posic.x + label.GetClientSizeTuple()[0],posic.y))
        elif etiq[:1]==']':     # Poner la etiqueta a la derecha del texto
            etiq=etiq[1:]
            label.SetPosition((posic.x + text.GetClientSizeTuple()[0],posic.y))
        else:   # Poner la etiqueta encima del texto
            label.SetPosition((posic.x,posic.y-15))
    #
    #-- Devuelve la Posicion actual de objeto
    #
    def GetPosition(self):
        """ Devuelve la posición actual del campo de texto como wx.Point """
        return self.__cttext.GetPosition()

    #
    #-- Cambia el tama�o del campo de texto
    #
    def SetSize(self,width,height=-1):
        if height==-1:
            height = self.__cttext.GetSize()[1]
        self.__cttext.SetSize(width,height)

    #
    #-- Devuelve el tama�o actual del campo de texto
    #
    def GetSize(self):
        """ Devuelve el tamaño actual del campo de texto como wx.Size """
        return self.__cttext.GetSize()

    #
    #-- Asigna un valor al Tip de Ayuda del campo de texto
    #
    def SetToolTipString(self,tip):
        """ Asigna un valor al Tip de Ayuda del campo de texto """
        self.__cttext.SetToolTip(tip)

    #
    #-- Pone editable / no editable el campo de texto
    #
    def SetEditable(self,bool):
        """ Pone Editable/No editable el campo de texto """
        self.__cttext.SetEditable(bool)

    #
    #-- Desactiva el campo de texto de la entrada
    #
    def Disable(self):
        """ Desactiva el campo de texto de la entrada"""
        self.__cttext.Disable()

    #
    #--- Devuelve el valor actual del campo de texto en su formato
    #
    def GetValue(self):
        """ Devuelve el valor actual de campo de texto en su formato """
        value = self.__cttext.GetValue()

        fmt = self._fmt
        lmax = self._lmax

        if fmt in ('0','1','2','3','4','5','6','7','8','9'):
            if value=='': value='0'
            value = float(value)
        elif fmt == 'i':
            if value=='': value='0'
            value = int(value)
        elif fmt =='d':
            value = Fecha_aNum(value)
        else:
            value = value.encode('latin-1')

        return value

    #
    #--- Asigna valor en su formato al campo de texto (convierte a cadena)
    #
    def SetValue(self,value,acc='s'):
        """ Asigna valor en su formato al campo de texto (convierte a cadena)"""
        fmt = self._fmt
        lmax = self._lmax
        #
        if value == None:
            value = ''
        elif fmt=='d':
            value = Num_aFecha(value)
        elif fmt in ('0','1','2','3','4','5','6','7','8','9'):
            if value=='': value=0.0
            else: value=float(value)
            value = str(round(value,int(fmt)))
        elif fmt == 'i':
            if value=='': value=0
            value = str(value)
        #
        vant = self.GetValue()
        if vant<>value: self._pb.Modifica=1
        #
        if type(value) <> unicode: value = value.decode('latin-1')
        self.__cttext.SetValue(value)
        #
        #
        if acc<>'n' and self._ade<>'':
            ls_ade = self._ade.split('|')
            for ade in ls_ade:
                ok = self._pb.Ejecuta_Accion(ade,self)
                if ok<0: return # La ejecución falló

    #
    #--- Cambia el valor del texto de la etiqueta
    #
    def SetLabel(self,value):
        self.__ctlabel.SetLabel(value)

    #
    #---Asigna el Foco al campo de texto
    #
    def SetFocus(self):
        """ Asigna el Foco al campo de texto """
        self.__cttext.SetFocus()

    #
    #-- Asignar Color de Fondo a la entrada de texto
    #
    def SetBackgroundColour(self,color):
        self.__cttext.SetBackgroundColour(color)

    #
    #-- Asignar Color de Fondo a la entrada de texto
    #
    def SetForegroundColour(self,color):
        self.__cttext.SetForegroundColour(color)

    #
    #
    #
    def Parent(self):
        return self.__cttext.Parent;

    #
    #--- Al Pulsar ENTER sobre el campo, formatea su valor (Fecha, % )
    #
    def Formatea_Valor(self):
        valor = self.__cttext.GetValue()
        fmt = self._fmt
        lmax = self._lmax
        #
        punto=False
        if self._pb<>None:
            try:
                if self._pb._idx == self._name and valor=='' or valor=='.':
                    valor = '.'
                    punto = True
            except:
                pass    # Si no tiene _idx daría fallo

        if not punto:
            if fmt=='%':
                if valor<>'': valor = valor.zfill(lmax)
            elif fmt=='d':
                fecha = Fecha_aNum(valor)
                if fecha==None:
                    mes = str(Fecha(fmt='m')).zfill(2)
                    anio = str(Fecha(fmt='y'))
                    if 0<len(valor)<=2:
                        valor = valor+'/'+mes+'/'+anio
                    elif len(valor)<5:
                        dia = valor[:2]
                        mes = valor[2:]
                        valor = dia+'/'+mes+'/'+anio
                    elif len(valor)>=6:
                        dia = valor[:2]
                        mes = valor[2:4]
                        anio= valor[4:]
                        if len(anio)==2: anio = '20'+anio
                        elif len(anio)==3: anio = '2'+anio
                        valor = dia+'/'+mes+'/'+anio
                    #
                    valor = Num_aFecha(Fecha_aNum(valor))
            elif fmt in ('1','2','3','4','5','6','7','8','9'):
                if valor=='': valor = '0'
                if valor.find('.')==-1: valor = valor+'.'
                ent,dec = valor.split('.')
                while len(dec)<int(fmt):
                    dec = dec + '0'
                valor = ent+'.'+dec

        self.__cttext.SetValue(valor)
        #
        return valor    # Se Utiliza en el grid.


    #
    #-- Evento al soltar tecla (Para controla accion al pulsar tecla)
    #
    def Al_Soltar_Tecla(self,event):
        if self._adk <> '':
            pb = self._pb
            pb.Ejecuta_Accion(self._adk,self)

    #
    #-- Evento al pulsar una tecla dentro del texto
    #
    def Al_Pulsar_Tecla(self,event):
        key = event.GetKeyCode()
        tipo = self._fmt
        pb = self._pb

        if event.ControlDown(): # .AltDown ; ShiftDown ; MetaDown
            if key==66: #B
                print 'Ctrl+B'

        elif key==wx.WXK_TAB:
            if self._dlsel<>'':
                self.OnDlgLeftDown(None)

        elif key==wx.WXK_ESCAPE:
            if self._name=='GRIDENTRY':
                pass
            else:
                pb.Prev_Ctrl(self)

        elif key==wx.WXK_LEFT:
            pos =self.__cttext.GetInsertionPoint()
            if pos==0:
                if self._name=='GRIDENTRY':
                    pass
                else:
                    pb.Prev_Ctrl(self)
            else:
                event.Skip()

        elif key==wx.WXK_RETURN or key==wx.WXK_NUMPAD_ENTER:
            if self._name=='GRIDENTRY':
                pass
            else:
                pb.Next_Ctrl(self)

        elif key==wx.WXK_RIGHT:
            pos = self.__cttext.GetInsertionPoint()
            max = len(self.__cttext.GetValue())
            if pos==max:
                if self._name=='GRIDENTRY':
                    pass
                else:
                    pb.Next_Ctrl(self)
            else:
                event.Skip()

        elif key==wx.WXK_DOWN:
            if self._name=='GRIDENTRY':
                #debug(actual._grid)
                pass
        elif key==wx.WXK_UP:
            if self._name=='GRIDENTRY':
                #debug(actual._grid)
                pass
        else:
            if key > 255:
                event.Skip()
                return
            char = chr(key)
            if char in string.printable:
                ok = IsValid(key,tipo,self.__cttext.GetValue())
                if not ok:
                    return          # Cancelamos el evento
                else:
                    pb.Modifica = 1
                    event.Skip()    # Dejamos continuar el evento

            else:
                event.Skip()

    #
    #-- Ejecutar la Formula de Cálculo
    #
    def Al_Entrar(self,event):
        """ Formula de Calculo """
        pb = self._pb
        if pb<>None:
            pb._cta = self  #event.GetEventObject()
            self._vant = self.GetValue()
            #
            if self._fcal<>'':
                valor = self.GetValue()
                if valor=='' or self._sobre.upper()=='S':
                    valor = self._pb.Ejecuta_Accion(self._fcal)
                    self.SetValue(valor)

        """ Mostrar el boton de seleccion se tiene dialogo """
        if self._dlsel<>'':
            pos = self.__cttext.GetPosition()
            size = self.__cttext.GetSize()
            imagen = DIR_IMG+'/16/dlgsele.png'
            posic = (pos.x+size[0],pos.y+5)
            img = wx.Image(imagen,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            tam = (img.GetWidth(), img.GetHeight())
            btn = wx.StaticBitmap(self.Parent(), -1, img, posic, tam)
            btn.Bind(wx.EVT_LEFT_DOWN, self.OnDlgLeftDown)

            self.__btnsel = btn

        event.Skip()

    def OnDlgLeftDown(self,event):
        pb = self._pb
        posme = self.GetPosition()
        pospb = pb.GetPosition()
        dlsel = self._dlsel
        if dlsel[:6]=='LISTA:':
            respu=''
            valores = dlsel[6:]
            if ']' in valores:
                if valores[-2]==']':
                    respu = valores[-1]
                    valores = valores[:-2]
            valores = valores.split('|')
            dlg = dlg_sele(self,valores,respu)
            # dlg.MakeModal()
            dlg.Show()
        else:
            import dl_sele
            fichero,inf = dlsel.split(',')
            dl_sele.dl_sele(pb,fichero,inf,self)


    #
    #-- Ejecutar Accion Despues de Editar
    #
    def Al_Salir(self,event):
        """ Acción Despues de Editar """
        self.Formatea_Valor()
        pb = self._pb
        if pb<>None:
            #
            tipo = self._fmt
            if tipo=='d':   # Comprobamos fecha correcta
                pass
            #
            if self._ade<>'':
                cta = pb._cta
                acciones = self._ade.split('|')
                for accion in acciones:
                    ok = pb.Ejecuta_Accion(accion,self)
                    if ok<0: # Ocurrió algún fallo
                        if self._name<>'GRIDENTRY':
                            self.SetValue(self._vant,'n')
                            cta.SetFocus()
                        else:
                            grid = self._grid
                            fil,col = grid.GetCursor()
                            grid.SetCursor(fil,col)

                        return False
        #
        """ Ocultar el boton de seleccion se tiene dialogo """
        if self.__btnsel<>None:
            self.__btnsel.Show(0)
            self.__btnsel.Destroy()
            self.__btnsel= None
        event.Skip()

##
##
##  --DIALOGO DE SELECCIÓN
##
##
class dlg_sele(wx.MiniFrame):
    def __init__(self,entry,valores,respu=''):
        posme = entry.GetPosition()
        #
        padre = entry._pb
        pospa = padre.GetPosition()
        ancho = entry.GetTextCtrl().GetSize()[0]
        alto = entry.GetTextCtrl().GetSize()[1]
        posic = (posme[0]+pospa[0]+ancho, posme[1]+pospa[1]+alto+100)

        wx.MiniFrame.__init__(self,padre,-1,'Seleccione',size=(100,150),pos=posic,
            style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        panel = wx.Panel(self, -1)
        #
        lb = wx.ListCtrl(self,-1,style=wx.LC_REPORT,size=(95,145),pos=(0,-25))
        ncol=0
        lb.InsertColumn(ncol,'')
        for valor in valores:
            nfila = lb.InsertItem(2,'??')
            lb.SetItem(nfila,ncol,valor)
        #
        lb.SetFocus()
        lb.Select(0,True)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.Aceptar,lb)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        #
        self.lista = lb
        self.entry = entry
        self.respu = respu      # Cuantos caracteres devolvemos

    def Aceptar(self,event):
        item = event.GetItem()
        sele = item.GetText()
        if self.respu<>'':
            n = int(self.respu)
            sele = sele[:n]

        if self.entry._name == 'GRIDENTRY':
            f = self.entry._grid.GetNRow()
            c = self.entry._grid.GetNCol()
            self.entry._grid.SetValue(sele,f,c)
        else:
            self.entry.SetValue(sele)

        self.entry._pb.Next_Ctrl(self.entry)
        self.entry.SetFocus()
        self.Destroy()

    def Pulsar(self,event):
        print('Entry','Pulsar',event.GetKeyCode())

    def OnCloseWindow(self, event):
        self.Destroy()

##
##--------------------------------------
##

if __name__ == "__main__":
    app = wx.App(False)
    #
    campos = []
    #
    lse=[]
    lse.append(['E1','Código',10,20,6,'%',7,'','','','','sel-ar','Formato %','',''])
    lse.append(['E2','Nombre',100,20,35,'l',25,'','','','','','Formato l','',''])
    lse.append(['E3','Fecha',500,20,10,'d',10,'','','','','','Formato d','',''])
    lse.append(['E4','Entero',10,100,10,'i',10,'','','','','','Formato i','',''])
    lse.append(['E5','Decimal 2',150,100,10,'2',10,'','','','','','Formato 2','',''])
    lse.append(['E6','Multilinea',300,100,30,'m4',15,'','','','','','Formato m4','',''])
    #
    campos.append(['ENTRYS','ENT',25,50,'','',lse])

    import Ventana
    ventana = Ventana.Ventana(None)
    ventana.init_ctrls(campos)
    ventana.Show()

    app.MainLoop()

