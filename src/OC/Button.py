#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import wx.lib.buttons as buttons
import os

from global_var import DIR_IMG

class Button():

    def __init__(self,pb,padre,nombre,posic,tamano,imagen,texto,accion,tip):
        #- Tipo de bot�n segun el tipo
        boton = None
        img = None
        texto = texto.decode('latin-1')
        tip = tip.decode('latin-1')

        #- Intentamos cargar la imagen para el bot�n
        if imagen<>'':
            if imagen in os.listdir(DIR_IMG+'/32/'):
                imagen = DIR_IMG+'/32/'+imagen

            try:
                img = wx.Image(imagen, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            except:
                imagen=''
        #
        if imagen<>'' and texto<>'': # Boton con Imagen y Texto
            boton = buttons.GenBitmapTextButton(padre,-1,img,texto)
        elif imagen<>'':    # Boton con imagen
            boton = buttons.GenBitmapButton(padre,-1,img)
        else:   # Boton con texto
            boton = buttons.GenButton(padre,-1,texto)

        #- Asignamos Propiedades
        boton.SetToolTip(tip)
        boton.SetSize(tamano)
        boton.SetPosition(posic)
        boton.SetBezelWidth(2)

        #- Asignamos el Evento
        boton.Bind(wx.EVT_BUTTON,self.onPressButton)
        boton.Bind(wx.EVT_ENTER_WINDOW,self.onMouseOn)
        boton.Bind(wx.EVT_LEAVE_WINDOW,self.onMouseOut)

        #
        self._name = nombre
        self.__pb = pb           # Padre Base, contiene la accion a ejecutar
        self.__boton = boton     # Objeto Boton
        self.__accion = accion   # Nombre de la accion a ejecutar


    #
    #-- Activar/Desactivar boton
    #
    def Enable(self,bool):
        """ Activar / Desactivar Boton """
        self.__boton.Enable(bool)

    #
    #-- Muestra / Oculta el boton
    #
    def Show(self,bool):
        """ Muestra / Oculta el boton """
        self.__boton.Show(bool)

    #
    #-- Asigna una nueva acci�n al boton
    #
    def SetAccion(self,accion):
        """ Cambia la acci�n a ejecutar del boton """
        self.__accion = accion

    #
    #-- Asigna una imagen al boton
    #
    def SetImage(self,wx_image):
        """ Asigna una imagen al boton """
        pass

    #
    #
    #
    def SetStyleText(self,style):
        """ Cambia el estilo del texto mostrado en el boton """
        pass

    def SetStyleButton(self,style):
        """ Cambia el estilo del bot�n """
        pass

    def GetButton(self):
        """ Devuelve el objeto boton """
        return self.__boton

    #
    #-- Evento al Pulsar el boton
    #
    def onPressButton(self,event):
        """ Evento al pulsar el boton """
        pb = self.__pb
        acc = self.__accion

           
        if pb<>None:
            lacc = acc.split('|')
            for acc in lacc:
                ok = pb.Ejecuta_Accion(acc)
                if ok==None: return
                if isinstance(ok,tuple):
                    if ok[0]==-1: return

    #
    #-- Pinta el bot�n al entrar el rat�n en su cuadro
    #
    def onMouseOn(self,event):
        self.__boton.SetBezelWidth(1)
        self.__boton.Refresh()

    #
    #-- Pinta el boton al salir el rat�n en su cuadro
    #
    def onMouseOut(self,event):
        self.__boton.SetBezelWidth(2)
        self.__boton.Refresh()


#- #################################################################
#-
#- #################################################################

class CheckButton():

    def __init__(self,pb,padre,id,posic,tamano,texto,accion=''):
        texto = texto.decode('latin-1')
        tamano = (tamano[0]*10, tamano[1]*10)

        check = wx.CheckBox(padre,-1,texto,posic,tamano)
        check.Bind(wx.EVT_CHECKBOX, self.OnChange)
        #
        self._name = id
        self.__pb = pb           # Padre Base, contiene la accion a ejecutar
        self.__button = check     # Objeto Boton
        self.__accion = accion   # Nombre de la accion a ejecutar


    def Enable(self,status):
        self.__button.Enable(status)

    def GetValue(self):
        activo = self.__button.GetValue()
        res = 0
        if activo: res=1
        return res

    def SetValue(self,state,tr='n'):
        #if state==1: state=True
        #else: state = False
        self.__button.SetValue(state)
        if tr<>'n':
            if self.__accion <> '':
                self.__pb.Ejecuta_Accion(self.__accion,self)

    def SetLabel(self,label):
        self.__button.SetLabel(label)

    def Show(self,status):
        self.__button.Show(status)

    def SetToolTip(self,texto):
        texto = texto.decode('latin-1')
        #self.__button.SetToolTip(texto)
        
    def SetFocus():
        pass

    def OnChange(self,event):
        pb = self.__pb
        acc = self.__accion

        if pb<>None:
            lacc = acc.split('|')
            for acc in lacc:
                ok = pb.Ejecuta_Accion(acc)
                if ok==None: return

        event.Skip()




#- #################################################################
#-
#- #################################################################

class RadioButton():

    def __init__(self,pb,padre,id,titulo,posic,tamano,valores,ncols=1,accion=''):
        titulo = titulo.decode('latin-1')
        valores = valores.decode('latin-1')
        #
        valores = valores.split('|')
        tamano = (tamano[0]*10, tamano[1]*10)

        radio = wx.RadioBox(padre,-1,titulo,posic,tamano,valores,ncols,wx.RA_SPECIFY_COLS)
        radio.Bind(wx.EVT_RADIOBOX, self.OnChange)
        #
        self._name = id
        self.__pb = pb           # Padre Base, contiene la accion a ejecutar
        self.__button = radio    # Objeto Boton
        self.__accion = accion   # Nombre de la accion a ejecutar


    def OnChange(self,event):
        pb = self.__pb
        acc = self.__accion

        if pb<>None:
            pb.Ejecuta_Accion(acc)

        event.Skip()

    def Enable(self,status):
        self.__button.Enable(opc)

    def SetValue(self,opc):
        self.__button.SetSelection(opc)

    def GetValue(self):
        return self.__button.GetSelection()

    def GetStringValue(self):
        return self.__button.GetStringSelection()

    def Active(self,opc):
        self.__button.ShowItem(opc,True)

    def DesActive(self,opc):
        self.__button.ShowItem(opc,False)



#- #################################################################
#-
#- #################################################################


if __name__ == "__main__":

    app = wx.PySimpleApp()
    frame = wx.Frame(None,title="Prueba de la Clase Boton")
    frame.SetSize((800,600))
    frame.CentreOnScreen()
    #
    p1 = wx.Panel(name='P1', parent=frame)
    #
    btn1 = Button(None,p1,'B1',(100,100),(60,40),'','Abrir','abrir','Abrir Archivo')
    btn2 = Button(None,p1,'B2',(200,100),(60,40),'','Cerrar','cerrar','Cerrar Archivo')
    btn2.GetButton().SetDefault()
    #
    radio = RadioButton(None,p1,"R1","Prueba",(100,300),(10,8),"Opcion1|Opcion2",1,"a_cambia")
    #
    check = CheckButton(None,p1,"C1",(400,300),(10,8),"MiCheck",'a_activa')
    #
    frame.Show()
    app.MainLoop()
