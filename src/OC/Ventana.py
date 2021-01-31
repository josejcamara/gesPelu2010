#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import bsddb
import shelve
import pickle
import Entry
import Grid
import List
import Button
from Funciones import debug
from Funciones import Men
from Funciones import Num_aFecha
from Funciones import copia_rg
import Funciones
import os


from global_var import DIR_BASE
from global_var import DIR_DATA
from global_var import DIR_APL
from global_var import DIR_IMG


class Ventana(wx.Frame):
    """Clase Ventana. Es un wx.Frame modificado para que acepte una lista
    con los campos a introducir en él:
        #-    INSERTAR PANELES:
            ['PANEL',nombre, xini, yini, tamanox, tamanoy,color, CAMPOS_HIJOS]
        #- INSERTAR ENTRADAS:
            ['ENTRY', alto_control, salto_a_-1, style_etiq, style_txt, LS_ENT]
               LS_ENT = [Nombre,etiq,xini,yini,formato,max,ancho,edi,
                               fcal,sobre,ade,dlsel,tip,cpan,style]
    """

    def __init__(self, parent, titulo='', campos=[] , tam=(800,600), show=True):
        """ Creación de la ventana (Frame) """

        #self._pb=None        # Ventana Padre, será siempre la actual
        self._ct = {}        # Lista de objetos incrustados en la ventana
        self._cta = None     # Objeto Actual que tiene el foco
        self._ctord =[]      # Nombres de los campos editables por orden de foco
        self.Modifica = 0    # Si tiene valor 1 es que se han modificado los valores de la ventana
        #
        self._parent=parent      # Ventana padre
        self._idx = ''       # Campo que contiene el codigo del archivo
        self._filedb = ''    # Nombre Archivo relacionado en base de datos
        self._filept = None  # Puntero al fichero de la base de datos, abierto si corresponde
        self._accini=''      # Acción al cargar la ventana
        self._accleer = ''   # Acción despues de leer registro
        self._btfin = ''     # Nombre del boton a ejecutar cuando pulse boton FIN
        self.__hash = 0      # Hash del registro leido

        tam = (tam[0],tam[1]+23)    # Añadimos el alto de la barra Estado
        titulo = titulo.decode('latin-1')
        
        class_name = self.__class__.__name__
        wx.Frame.__init__(self, parent, name=class_name, title=titulo, size = tam)

        self.CenterOnScreen()

        self._statusbar = self.CreateStatusBar()

        try:
            self.SetIcon(wx.Icon(DIR_BASE+'/wico.ico',wx.BITMAP_TYPE_ICO))
        except:
            pass

        

        self.Bind(wx.EVT_CLOSE,self.onClose)

        if show: self.Show(True)

    #
    #
    #
    def onClose(self,evt):
        if self._filept <>None:
            self._filept.close()
            
        if self._parent <> None:
            self._parent.Show(1)

        self.Destroy()



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

        for lnc in campos:
            tipo = lnc[0]

            #- INSERTAR PESTAÑAS
            if tipo=='TABBOX':
                self.__Pon_NoteBook(padre,lnc)

            #- INSERTAR PANELES
            # ['PANEL',nombre, xini, yini, tamanox, tamanoy,color,lista_hijos]
            elif tipo=='PANEL':
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

        #print "Controles inicializados."
        ## SE EJECUTA VARIAS VECES EN RECURSIVIDAD !!!
        ##self.Refresh()
        ##self.Ejecuta_Accion(self._accini)

    #
    #-- Acciones Estandar para las ventanas
    #
    def Ejecuta_Accion(self,accion,obj=None,args=None):
        """ Acciones Estandar para las ventanas """
        valor = accion
        aux = accion.split(':')
        accion = aux[0]
        arg=[]
        if args<>None:
            arg = args
        else:
            if len(aux)>1: arg = aux[1].split(',')


        cta = self._cta
        if obj<>None: cta = obj

        if accion=='a_SALIR':
            if self.Modifica==1:
                dlg=Men('Ha realizado cambios en la ficha\n¿Desea Continuar sin grabar?','sn','q')
                if dlg=='n': return (1,'')  # Accion Ejecutada
            #-
            self.Close()
            self.Destroy()
            return (1,'')

        elif accion=='a_CPAN':
            import sys

            ventana = arg[0]
            win = wx.FindWindowByName(ventana)
            print win
            if win:
                win.Hide()
                win.Show()
                #win.RequestUserAttention() --> La marca y parpadea...
                return

            code = 'import '+ventana+'\n'
            code +='dlg = '+ventana+'.'+ventana+'()\n'
            exec(code)
            return (1,'')

        file = self._filedb
        ruta_datos = DIR_DATA +'/'+ file + '.db'
        try:
            idx = self._ct[self._idx].GetValue()
            idx = str(idx)
            if idx=='': idx='.'
        except:
            idx=''
        #
        if file<>'' and self._filept==None:
            self._filept = bsddb.btopen(ruta_datos)

        res = None   # Si es igual a None, no se ejecutó accion
        if accion=='a_LEE_RG':
            if self.Modifica==1 and cta._vant<>'':
                dlg=Men('Ha realizado cambios en la ficha\n¿Desea Continuar sin grabar?','sn','q')
                if dlg=='n': return (1,'')  # Accion Ejecutada
            #-
            self.Modifica = 0
            self.__hash = 0
            cod = str(cta.GetValue())
            if cod<>'' and cod<>'.':
                fich = self._filept    
                if not cod in fich.keys():
                    avisa=1
                    if len(arg)>0:
                        if arg[0] == 'n': avisa=0
                    if avisa: Men('No existe el registro '+cod+' en '+self._filedb)
                    self.Limpia_Pantalla('n')
                    self.__hash = 0
                else:
                    self.Reg_aPan(fich[cod])
                    self.__hash = fich[cod].__hash__()

            self.Modifica=0
            res=(1,'')

        elif accion=='a_GRABA':
            #
            if len(arg) > 0:
                if arg[0]<>'':  # Accion antes de grabar
                    ok = self.Ejecuta_Accion(arg[0])
                    if ok==-1:
                        return (-1,'')   # Operacion cancelada
                    
                # Volver a leer despues de grabar?
                voleer = 1
                if len(arg)>1: 
                    if arg[1]=='n': voleer = 0
            #
            if file=='':
                Men('No ha definido tabla sobre la que grabar.')
                return (-1,'')
            if idx=='':
                Men('No se ha definido correctamente el campo codigo de registro')
                return (-1,'')
            #
            if self.Modifica==0:
                msj = 'No ha realizado cambios.\12¿Desea guardar el registro?'
                dlg = Men(msj,'sN','q')
                if dlg=='n': return (1,'')

            rg_new = self.Pan_aReg()
            if rg_new==None: return(0,'No se pudo leer datos de pantalla.')

            #- Está definida la tabla en los diccionarios de aplicacion??
            dicc = bsddb.btopen(os.path.join(DIR_APL,'dicc'))
            if not file in dicc:
                Men('No existe la tabla '+file+'\nNo se puede guardar.')
                return (-1,'')
            midicc = pickle.loads(dicc[file])   # Propiedades del Diccionario
            accion = midicc[4]  # Acción al grabar
            ndig = midicc[1]    # Nº de digitos de la clave del dicc
            dicc.close()

            f = self._filept   
            fkeys = f.keys()
            # Se ha anticipado alguien?
            if idx in fkeys:
                if self.__hash <> f[idx].__hash__():
                    Men('No es posible grabar. Alguien se anticipó')
                    return (-1,'')

            # Busqueda del ultimo codigo libre
            if idx=='.':
                claves = fkeys
                claves.sort()
                if claves==[]:
                    idx='0'*ndig
                else:
                    idx=claves[-1]
                    idx = str(int(idx) +1).zfill(ndig)

            if accion<>'':  # Hay accion al grabar... la ejecutamos
                if idx in fkeys:   # El registro ya existe, desactualizamos
                    self._signo=-1
                    rg_old=pickle.loads(f[idx])
                    self._rg = copia_rg(rg_old) # Registro antiguo
                    self.Ejecuta_Accion(accion)

                # Actualizamos con el valor nuevo del registro
                self._signo=1
                self._rg = copia_rg(rg_new)
                self.Ejecuta_Accion(accion)
                rg = self._rg   # Cogemos los valores nuevos

            else:           # No hay accion al grabar... simplemente grabamos
                rg = rg_new
            #-

            f[idx] = pickle.dumps(rg)
            f.sync()
            
            #-
            Men('Registro '+idx+' guardado',img='i')
            
            # Recargar el registro
            if self._ct[self._idx].GetFmt() == 'd': idx = int(idx)
            try:
                if voleer: self._ct[self._idx].SetValue(idx)  
                else: self._ct[self._idx].SetValue(idx,'n')  
            except:
                self._ct[self._idx].SetValue(idx,'n')  
            self.__hash = pickle.dumps(rg).__hash__()
            self.Modifica=0
            res=(1,'')

        elif accion=='a_NEXT':
            if self.Modifica==1:
                dlg =Men('Ha realizado cambios en la ficha\n¿Desea Continuar sin grabar?','sn','q')
                if dlg=='n': return (1,'')

            f = self._filept   
            lsk = f.keys()
            lsk.sort()
            
            if lsk==[]:
                Men('No hay registros en la tabla '+file)
                return (1,'')
            nidx = lsk[0]
            if idx in lsk:
                pos = lsk.index(idx)
                if pos==len(lsk)-1:
                    Men('No hay registro siguiente a '+idx)
                    return (1,'')
                nidx= lsk[pos+1]

            self._ct[self._idx].SetValue(nidx)
            self.Modifica=0
            res=(1,'')

        elif accion=='a_PREV':
            if self.Modifica==1:
                dlg =Men('Ha realizado cambios en la ficha\n¿Desea Continuar sin grabar?','sn','q')
                if dlg=='n': return (1,'')

            f = self._filept   
            lsk = f.keys()
            lsk.sort()

            if lsk==[]:
                Men('No hay registros en la tabla '+file)
                return (1,'')
            nidx = lsk[-1]
            if idx in lsk:
                pos = lsk.index(idx)
                if pos==0:
                    Men('No hay registro anterior a '+idx)
                    return (1,'')
                nidx= lsk[pos-1]
            
            self._ct[self._idx].SetValue(nidx)
            self.Modifica=0
            res=(1,'')

        elif accion=='a_NUEVO':
            if self.Modifica==1:
                dlg =Men('Ha realizado cambios en la ficha\n¿Desea Continuar sin grabar?','sn','q')
                if dlg=='n': return (1,'')
            self.Limpia_Pantalla(otros=arg)
            self._ct[self._ctord[0]].SetFocus()
            self.Modifica=0
            res=(1,'')

        elif accion=='a_BORRA':
            tipo = self._ct[self._idx]._fmt
            cod = self._ct[self._idx].GetValue()
            if cod=='' or cod=='.':
                Men('No ha indicado el código de registro a borrar')
                return (-1,'')
            if tipo=='d': cod = Num_aFecha(cod)
            else: cod = str(cod)
            #
            #- Accion antes de borrar
            if len(arg) > 0:
                if arg[0]<>'':  
                    ok = self.Ejecuta_Accion(arg[0])
                    if ok==-1:
                        return (-1,'')   # Operacion cancelada
            #
            dlg = Men('¿Está seguro de borrar el registro '+cod+'?','sn','q')
            if dlg=='n': return (1,'')
            #- Propiedades de la tabla a trabajar
            dicc = bsddb.btopen(os.path.join(DIR_APL,'dicc'))
            if not file in dicc:
                Men('No se ha definido la tabla '+file+'\nNo se puede guardar.')
                return (-1,'')
            midicc = pickle.loads(dicc[file])
            dicc.close()

            # Acción para grabar (desactualizar)
            f = self._filept   
            accion = midicc[4]
            if accion<>'':
                self._signo=-1
                self._rg = pickle.loads(f[idx])
                self.Ejecuta_Accion(accion)
            # Borrar el registro
            f[idx]=''
            del f[idx]

            Men('Registro '+idx+' borrado.',img='i')
            self.Limpia_Pantalla()
            self._ct[self._ctord[0]].SetFocus()
            self.Modifica=0
            res=(1,'')

        elif accion=='a_SELE':
            valor = cta.GetValue()
            opciones = arg[0].split('+')
            if not valor in opciones:
                Men('Valor '+str(valor)+' no válido. Solo admite '+','.join(opciones))
                res = (-1 ,'')  # Se ejecutó pero mal.
            else:
                res=(1,'')

        elif accion=='a_INFO':
            if len(arg)>0: fichero = arg[0]
            else: fichero=self._filedb
            informe,destino = '',''
            if len(arg)>1: informe = arg[1]
            if len(arg)>2: destino = arg[2]
            if informe=='':
                import dl_select
                dlg = dl_select.dl_sel_inf(self,fichero)
                informe = dlg.res()
            #
            if informe=='':return (1,'')
            Funciones.Crea_Info(self,fichero,informe,destino)

        elif accion=='c_CAMPOS':
            lscampos = arg[0]
            lscampos = lscampos.split(' ')
            for campo in lscampos:
                fcal = self._ct[campo]._fcal
                if fcal<>'':
                    val = self.Ejecuta_Accion(fcal,self._ct[campo])
                    self._ct[campo].SetValue(val)
            res=(1,'')

        elif accion=='a_CREA_INFO':
            res=(1,'')

        if res==None:
            res=(0,'')  # NO SE EJECUTÓ NINGUNA ACCION
        else:
            res=(1,res) # SE EJECUTÓ LA ACCION, CON ESTE RESULTADO

        return res

    #
    #-- Pintar un Panel para Pestañas en la Ventana
    #
    def __Pon_NoteBook(self,padre,datos):
        """ Pinta en la Ventana un Panel para poner Pestaña (Tabbox)
        ['TABBOX',Id, xini, yini, tamanox,tamanoy, style, borde
        Titulo(Si pestaña)/Accion al cambio(Si Tabbox), CAMPOS_HIJOS]
        """
        tipo = datos[0]
        if tipo<>'TABBOX':
            return -1

        nombre = datos[1]
        xini, yini = int(datos[2]), int(datos[3])
        tamx,tamy = int(datos[4]), int(datos[5])
        #estilo = datos[6]
        #borde = datos[7]
        #acciontb = datos[8]
        hijos = datos[-1]

        posic = wx.Point(xini,yini)
        if tamx==-1: tamx = padre.GetSize()[0]
        if tamy==-1:
            tamy = padre.GetSize()[1] - self._statusbar.GetSize()[1]
            if padre==self: tamy = tamy - 30    # Quitamos el tamaño del titulo

        tam = wx.Size(tamx,tamy)
        #
        elem = wx.Notebook(name=nombre, parent=padre, pos=posic, size=tam)
        #
        if hijos<>[]:
            for hijo in hijos:
                p = self.__Pon_Panel(elem, hijo)
                elem.AddPage(p,hijo[8].decode('latin-1'))

        #- Ponemos en el diccionario de campos
        if not nombre in self._ct:
            self._ct[nombre]=elem
        else:
            debug('El control '+nombre+' se encuentra repetido.')

        return elem

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
        borde = datos[7]
        #acciontb = datos[8]
        hijos = datos[-1]

        posic = wx.Point(xini,yini)
        if tamx==-1: tamx = padre.GetSize()[0]
        if tamy==-1:
            tamy = padre.GetSize()[1] - self._statusbar.GetSize()[1]
            if padre==self: tamy = tamy - 30    # Quitamos el tamaño del titulo

        tam = wx.Size(tamx, tamy)
        #-
        if tipo=='PANEL':
            pestilo = wx.TAB_TRAVERSAL
            if borde in (1,'1'): pestilo |= wx.SIMPLE_BORDER
            elif borde in (2,'2'): pestilo |= wx.SUNKEN_BORDER
            elif borde in (3,'3'): pestilo |= wx.RAISED_BORDER
            elem = wx.Panel(name=nombre, parent=padre, pos=posic, size=tam, style=pestilo)
        elif tipo=='TABBOX':
            elem = wx.Notebook(name=nombre, parent=padre, pos=posic, size=tam)
        else:
            elem = None
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

        return elem

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
            if xini=='': xini='-1'
            if yini=='': yini='-1'
            if ancho=='': ancho='10'
            if max=='': max=0
            #-
            xini,yini = int(xini),int(yini)
            ancho,max = int(ancho),int(max)

            #-- Asignar Posicion cuando se indica pos -1
            auto=0
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
                xini,yini = 5, ulty + salto
                posic = wx.Point(xini,yini)
                elem.SetPosition(posic)

            # Posicion del ultimo campo
            ultx,ulty = xini, yini
            if dlsel<>'': ultx+=10
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

        grid = Grid.Grid(self,padre,nombre,(posx,posy),ancho,hfila,nfilas,cols,wfilat,filast,props,titu=titulo)

        #- Ponemos en el diccionario de campos
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
            #texto = texto.decode('latin-1')
            #tip = tip.decode('latin-1')
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
        if not id in self._ct:
            self._ct[id]=elem
        else:
            Men('El control '+id+' se encuentra repetido.')

    #
    #-- Escribe el texto indicado en la barra de estado
    #
    def SetStatusText(self,text):
        """ Escribe el texto indicado en la barra de estado """
        text = text.decode('latin-1')
        self._statusbar.SetStatusText(text)

    #
    #--
    #
    def Pan_aReg(self):
        """ Convierte los datos de la pantalla en un diccionario """
        reg = {}
        ct = self._ct
        lsord = self._ctord
        filedb = self._filedb

        #- Obtenemoslos campos de la definicion del diccionario
        dicc = bsddb.btopen(os.path.join(DIR_APL,'dicc'))
        if not filedb in dicc:
            Men('No se ha definido la tabla '+filedb+'\nNo se puede guardar.')
            return None
        campos = pickle.loads(dicc[filedb])[-1] # Ultima posicion tiene la lista de campos
        dicc.close()
        for ln in campos:
            key,deno,fmt = ln[:3]
            if key in ct:
                reg[key]=ct[key].GetValue()
            else:
                if fmt in ('l','%'): reg[key]=''
                elif fmt in ('i','0','1','2','3','4','5','6','7','8','9'): reg[key]=0
                elif fmt in ('d'): reg[key]=None
                else: reg[key]=[]

        return reg

    #
    #-- Pasar un registro a pantalla
    #
    def Reg_aPan(self,reg):
        reg = pickle.loads(reg)
        for campo in reg.keys():
            if campo in self._ct.keys():
                self._ct[campo].SetValue(reg[campo]) #,'n')
    #
    #-- Moverse al siguiente campo de la ventana
    #
    def Next_Ctrl(self,actual):
        lsct = self._ctord
        if actual._name == 'GRIDENTRY':
            actual._grid.Next_Cell()
        else:
            tab = lsct.index(actual._name)
            if tab<len(lsct)-1:
                self._ct[lsct[tab+1]].SetFocus()
    #
    #-- Moverse al siguiente campo de la ventana
    #
    def Prev_Ctrl(self,actual):
        lsct = self._ctord
        if actual._name == 'GRIDENTRY':
            actual._grid.Prev_Cell()
        else:
            tab = lsct.index(actual._name)
            if tab>0:
                self._ct[lsct[tab-1]].SetFocus()

    #
    #-- Devuelve el valor de una formula de calculo
    #
    def Valor_FC(self,str_formula):

        valor = ""

        if str_formula[:6]=='cache(':   # Cargar dato de cache
            file,cod,campo = str_formula[6:-1].split(',')
            ruta_datos = DIR_DATA +'/'+ file + '.db'
            fich = bsddb.btopen(ruta_datos)
            if cod in fich.keys():
                rg = pickle.loads(fich[cod])
                valor = rg[campo]
            fich.close()
        else:
            valor = eval(str_formula)

        return valor

    #
    #-- Limpiar todos los campois dela pantalla
    #
    def Limpia_Pantalla(self,borra_idx='s',otros=[]):
        filedb = self._filedb
        campos = self._ct.keys()
        dicc = bsddb.btopen(os.path.join(DIR_APL,'dicc'))
        if filedb in dicc:
            campos = []
            for campo in pickle.loads(dicc[filedb])[-1]: # Ultima posicion tiene la lista de campos
                campos.append(campo[0])

        dicc.close()
        
        campos.extend(otros)

        for campo in self._ct.keys():   # Recorremos todos los campos de la ventana, continue si no interesa
            if borra_idx=='n' and campo==self._idx: continue
            if campo<>self._idx and campo not in campos: continue
            if isinstance(self._ct[campo],Entry.Entry): self._ct[campo].SetValue('','n')
            elif isinstance(self._ct[campo],Grid.Grid): self._ct[campo].SetValue([])
            elif isinstance(self._ct[campo],List.List): self._ct[campo].SetValue([])
            elif isinstance(self._ct[campo],Button.CheckButton): self._ct[campo].SetValue(False,'n')





#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":

    ls_campos=[]
    #
    p1 = ['PANEL','P1',0,0,-1,-1,'B-236:44:26/RF','','',[]]
    hijosp1=[]
    hijosp1.append(['E1','Código',10,15,6,'%',7,'','','','c_CAMPOS:E2 E3','ar_ls','codigo del cliente','clientes',''])
    hijosp1.append(['E2','Nombre',150,15,30,'l',10,'n','1','','','','','',''])
    hijosp1.append(['E3','Otro',-1,15,6,'l',10,'','2','','','','','',''])
    p1[-1].append(['ENTRYS','EX',22,50,'','',hijosp1])


    # PANELES: ['PANEL',nombre, xini, yini, tamanox, tamanoy,color,lista_hijos]
    ls_campos.append(p1)

    app = wx.PySimpleApp()
    ventana = Ventana(None)
    ventana.init_ctrls(ls_campos)
    ventana.Show()
    app.MainLoop()
