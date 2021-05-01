#!/usr/bin/env python
# -*- coding: utf8 -*-

import wx,os
import OC
import bsddb
import pickle
from OC.Funciones import *

class Manage_Win(OC.Ventana):
    """ Ficha para manejar las ventanas de la aplicación """
    
    def __init__(self,filePath):
        #
        self.filePath = filePath
        self.fileName = os.path.join(filePath,'wins')
        #
        OC.Ventana.__init__(self, None,'Ventanas de la Aplicacion',tam=(800,600))
        #
        self.NOMBRE_ROOT = 'Propiedades Generales'
        ls_campos = []
        
        # P0 - Lista de ventanas disponible
        p0 = ['PANEL','P0',0,0,200,150,'','','',[]]
        cols=[['Ventana','l'],['Descripción','l']]
        ls = ['LIST','L1',0,0,-1,-1,cols,'','','','','a_sele_win','','']
        p0[-1].append(ls)
        
        #P1- Arbol de objetos de la ventana seleccionada
        p1 = ['PANEL','P1',0,150,200,420,'','','',[]]
        #---
        # PONER ARBOL -> MAS ABAJO....
        #

        # P2 - Propiedades del Objeto
        p2 = ['PANEL','P2',200,0,600,500,'','','',[]]
        #---
        cols = []
        cols.append(['Propiedad',30,'l',0,'n','','','','','','','','',''])
        cols.append(['Valor',22,'l',0,'','','','','a_graba_cambio','','','','',''])
        #
        p2[-1].append(['GRID','G1','',8,75,590,22,15,cols,1,'',''])
        
        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',200,500,600,70,'','','',[]]
        btn=[]
        btn.append(['B1',10,10,80,'new.png','Nuevo','a_nuevo','Crear una nueva tabla',''])
        btn.append(['B2',110,10,80,'save.png','Grabar','a_graba','Grabar cambios en la tabla',''])
        btn.append(['B3',210,10,80,'','Borrar','a_borra','',''])
        btn.append(['B4',310,10,80,'','Ejecutar','a_ejecuta','',''])
        btn.append(['B9',510,10,80,'salir.png','Salir','a_salir','',''])
        p3[-1].append(['BUTTONS','BID',50,'','',btn])
        
        #
        ls_campos.append(p0)
        ls_campos.append(p1)
        ls_campos.append(p2)
        ls_campos.append(p3)
        #
        self.init_ctrls(ls_campos)
        
        self._ct['G1'].SetDialog('dl_entrys',1,1)
        
        #- TITULO DE LA VENTANA SELECCIONADA
        titu = wx.StaticText(self._ct['P2'],-1,"SELECCIONA VENTANA",(10,10),(20,50),wx.ALIGN_CENTER)
        titu.SetBackgroundColour('black')
        titu.SetForegroundColour('white')
        titu.SetFont(wx.Font(18,wx.DECORATIVE,wx.ITALIC,wx.NORMAL))
        self.titu = titu    # Indicador de Ventana Seleccionada
        
        #- PONER ARBOL
        ppadre =self._ct['P1']
        arbol = wx.TreeCtrl(ppadre)
        arbol.SetSize(ppadre.GetSize()) 
        self.arbol = arbol    # Arbol de Componentes de la ventana
        self.wsele = None     # Ventana Seleccionada
        self.data = {}        # Diccionario data[nodo]=datos_nodo
        
        #- Evento a seleccionar un elemento del arbol
        arbol.Bind(wx.EVT_TREE_SEL_CHANGED,self.onSeleTree,arbol)
        
        #- POPUP MENU PARA EL ARBOL
        popup = wx.Menu()
        opciones = ['Añadir Elemento','Eliminar Elemento']
        for opc in opciones:
            item = popup.Append(-1,opc)
            self.Bind(wx.EVT_MENU,self.onPopupSele,item)
        arbol.Bind(wx.EVT_CONTEXT_MENU,self.onShowPopup)
        self.popup = popup
        
        #---
        self.Ejecuta_Accion('a_carga_wins')
        
    #
    #--
    #
    def onSeleTree(self,evt):
        ventana = self.wsele
        if ventana==None:
            Men('No ha seleccionado ninguna ventana')
            return -1
        
        item = evt.GetItem()
        raiz = self.arbol.RootItem
        #
        titus=[]
        sele_cell = {}  # Dialogo de selección por celda
        if item==raiz:
            datos = self.data[self.NOMBRE_ROOT]
            titus = ['Descripción','Ventana Padre','Icono','Título Ventana']
            titus.extend(['Tamaño X','Tamaño Y','PosX','PosY'])
            titus.extend(['Tabla Asociada','Campo IDX'])
            titus.extend(['Accion Al Cargar','Accion Despues Leer','Boton al FIN'])
        else:
            id = self.arbol.GetItemText(item)
            datos = self.data[id]

            tipo = datos[0]
            if tipo=='PANEL':
                titus = ['Tipo','ID','X inicio','Y inicio','Ancho','Alto']
                titus.extend(['Color+Font','Borde','Titulo (Si Tabbox)'])
            elif tipo=='TABBOX':
                titus = ['Tipo','ID','X inicio','Y inicio','Ancho','Alto']
                titus.extend(['Color+Font','Borde','Accion al Cambio'])
            elif tipo=='ENTRYS':
                titus = ['Tipo','ID','Alto','Salto Y cuando -1']
                titus.extend(['Estilo Etiqueta','Estilo Entrada'])
                titus.extend(['Lista Entradas'])
                ## LISTA ENTRADAS:
                #    ID, Etiq X, Y, Ancho, Fmt, LMax, Edi, FC, Sobre, ADE 
                #    Dialogo, Tip, CPAN, Estilo
                sele_cell[(6,1)]='a_detalle_entradas'
            elif tipo=='LIST':
                titus = ['Tipo','ID','X inicio','Y inicio','Ancho','Alto']
                titus.extend(['Columnas','Anchos Fijos Columnas'])
                titus.extend(['Estilo','Seleccion Multiple?','Borrado?'])
                titus.extend(['Acción al Seleccionar','Accion Doble Click'])
                titus.extend(['Acción al Borrar'])
                ## COLUMNAS: [['Titulo','Formato']]
            elif tipo=='GRID':
                titus = ['Tipo','ID','Titulo','X inicio','Y inicio']
                titus.extend(['Ancho','Alto Fila','Nº Filas','Columnas'])
                titus.extend(['Ancho Titulo Fila','Titulos Filas'])
                titus.extend(['Propiedades Generales'])
                ## COLUMNAS:
                #    Nombre, Ancho, Fmt, lmax, Edit, Grabab,
                #    FC, Sobre, ADE, dl-sel, Totales, Tip, CPan, Style
            elif tipo=='BUTTONS':
                titus = ['Tipo','ID','Alto','Estilo','Arco','Lista Botones']
                # LISTA BOTONES: 
                #    ID, X, Y, Ancho, Imagen, Texto, Accion, Tip, Tecla
            elif tipo=='CHECK':
                titus = ['Tipo','ID','X','Y','Ancho','Alto','Titulo']
                titus.extend(['Valor Inicial','Accion al cambiar'])
            elif tipo=='RADIO':
                titus = ['Tipo','ID','X','Y','Ancho','Alto','Titulo']
                titus.extend(['Direccion','Valores (SEP = |)'])
                titus.extend(['Valor Inicial','Accion al Cambiar'])
            elif tipo=='TABBOX':
                titus = ['Tipo','ID','X inicio','Y inicio','Ancho','Alto']
                titus.extend(['Color+Font','Borde','Accion al Cambio'])
            elif tipo=='TEXT':
                titus = ['Tipo','ID','X inicio','Y inicio','Ancho','Alto']
                titus.extend(['Color+Font','Color+Font con Ratón','Borde'])
                titus.extend(['Alineamiento','Acción al Click'])
        #
        i=0
        g1=[]
        ntitus,ndatos = len(titus),len(datos)
        maxf = max(ntitus,ndatos)
        for i in range(maxf):
            titu,valor='????',''
            if ntitus>i: titu = titus[i]
            if ndatos>i: valor = datos[i]
            g1.append([titu,valor])
        #
        self._ct['G1'].SetValue(g1)
        self._ct['G1']._seleCell = sele_cell
        
    #
    #-- Mostrar Menu Popup del Arbol
    #
    def onShowPopup(self,evt):
        pos = evt.GetPosition()
        pos = self.arbol.ScreenToClient(pos)
        self.arbol.PopupMenu(self.popup,pos)
        
    #
    #-- Seleccionar Elemento del menu Popup del arbol
    #
    def onPopupSele(self,evt):
        id = evt.GetId()    # Id del menú popup
        #item = self.popup.FindItemById(id)
        #text = item.GetText()
        #ventana = self.wsele
        arbol = self.arbol
        data = self.data

        nodo = arbol.GetSelection()
        txtnodo = arbol.GetItemText(nodo)
        raiz = arbol.RootItem
        
               
        if id==100: # Añadir Elemento
            if nodo<>raiz:
                tipo = data[txtnodo][0]
                if tipo in ('LIST','GRID'):
                    Men('No puede añadir hijos a este elemento')
                    return
            
            ops=['Panel','Texto','Entrada','Lista','Grid','Botones']
            res = List_dlg(self,choices=ops)
            if res==-1: return
            sele = ops[res]
            
            idnodo = Entra_dlg(self,'Id Elemento','Introduce el ID del elemento')
            if idnodo==-1: return
            if idnodo=='':
                Men('Debe introducir un nombre para identificar el elemento.')
                return
            if idnodo in data.keys():
                Men('Ya existe un nodo con ese identificador.')
                return
            idnodo = idnodo.upper()
            if sele=='Panel':
                data[idnodo]=['PANEL',idnodo,'0','0','-1','-1','','','']
            elif sele=='Tabbox':
                data[idnodo]=['TABBOX',idnodo,'0','0','-1','-1','','','']
            elif sele=='Texto':
                data[idnodo]=['TEXT',idnodo,'0','0','10','22','','','','','']
            elif sele=='Entrada':
                data[idnodo]=['ENTRYS',idnodo,'22','50','','',[]]
            elif sele=='Lista':
                cols = []
                data[idnodo]=['LIST',idnodo,'0','0','100','100',cols,[],'','n','n','','','']
            elif sele=='Grid':
                cols = []
                data[idnodo]=['GRID',idnodo,'Titulo','0','0','100','22','5',cols,'1',[],'']
            elif sele=='Botones':
                data[idnodo]=['BUTTONS',idnodo,'40','','',[]]
            else:
                Men('Ha elegido un elemento no válido.')
                return
            #
            arbol.AppendItem(nodo,idnodo)
            arbol.Expand(nodo)

        elif id==101:   # Eliminar Elemento
            if nodo==raiz:
                Men('No puede borrar el elemento raiz')
                return
            dlg = Men('¿Está seguro de borrar el elemento?','sn',img='q')
            if dlg=='n': return
            del data[txtnodo]   # No borra los hijos,pero no es necesario
            arbol.Delete(nodo)
        else:
            Men('No se encontró accion para opcion seleccionada.')
        
        self.arbol.Expand(self.arbol.RootItem)
    
    #
    #-- Crear un Arbol con los Datos guardados en el diccionario
    #
    def Datos_a_Arbol(self,datos,parentItem=None):
        arbol = self.arbol
        #
        if parentItem==None:
            if arbol.RootItem.IsOk(): 
                arbol.DeleteChildren(arbol.RootItem)
            else:
                arbol.AddRoot(self.NOMBRE_ROOT)
            self.data={}
            #
            parentItem = arbol.RootItem
            self.data[self.NOMBRE_ROOT]=datos[:-1]
            hijos = datos[-1]
        else:
            hijos = datos
        #
        for item in hijos:
            tipo,id = item[0],item[1]
            nodo = arbol.AppendItem(parentItem,id)
            if tipo in ('PANEL','TABBOX'):
                self.data[id] = item[:-1]
                hijos2 = item[-1]
                if hijos2<>[]:
                    self.Datos_a_Arbol(hijos2,nodo)
            else:
                self.data[id] = item
                hijos2 = []
        #
        return self.data
        #
    #
    #
    #
    def Arbol_a_Datos(self,nodo=None):
        arbol = self.arbol
        data = self.data
        #
        if nodo == None: nodo = arbol.RootItem
        #
        if not nodo.IsOk(): return
        id = arbol.GetItemText(nodo)
        refs=[]
        refs.extend(data[id])
        #
        #
        child,cookie = arbol.GetFirstChild(nodo)
        xxx=[]
        while child.IsOk():
            if arbol.ItemHasChildren(child):
                dhijos=self.Arbol_a_Datos(child)
            else:
                id = arbol.GetItemText(child)
                dhijos=data[id]
                if data[id][0] in ('PANEL','TABBOX'):
                    dhijos.append([])

            child,cookie = arbol.GetNextChild(child,cookie)
            xxx.append(dhijos)
            #
        refs.append(xxx)

        return refs           
                    
    #
    #
    #
    def Ejecuta_Accion(self,accion,argumentos=''):
        if accion=='a_salir':
            if self.Modifica==1:
                dlg = Men('Hay cambios en la ventana y no ha guardado.\n¿Desea Continuar?','sn',img='q')
                if dlg=='n': return
            self.Modifica = 0
            self.Close()
            self.Destroy()
            #
        elif accion=='a_carga_wins':
            if self.Modifica==1:
                dlg = Men('Hay cambios en la ventana y no ha guardado.\n¿Desea Continuar?','sn',img='q')
                if dlg=='n': return
            self.Modifica = 0
                
            """ Leer la lista de ventanas actuales """
            lis=[]
            wins = bsddb.btopen(self.fileName)
            for nm in wins.keys(): 
                datos = pickle.loads(wins[nm])
                lis.append([nm,datos[0]]) # Ventana, Descripcion
            wins.close()
            #
            self._ct['G1'].SetValue([])
            self.arbol.DeleteAllItems()
            
            self._ct['L1'].SetValue(lis)
            #
        elif accion=='a_sele_win':
            #
            if self.Modifica==1:
                dlg = Men('Hay cambios en la ventana y no ha guardado.\n¿Desea Continuar?','sn',img='q')
                if dlg=='n': return
            self.Modifica = 0
            #
            sele = self._ct['L1'].GetValue()
            if sele==None:
                Men('No hay seleccionada ventana')
                return -1
            #
            wins = bsddb.btopen(self.fileName)
            datos = pickle.loads(wins[sele])
            wins.close()
            #
            self.Datos_a_Arbol(datos)
            #
            self.wsele= sele
            self.titu.SetLabel(sele.upper())
            self.arbol.SelectItem(self.arbol.RootItem)

            
        elif accion=='a_nuevo':
            if self.Modifica==1:
                dlg = Men('Hay cambios en la ventana y no ha guardado.\n¿Desea Continuar?','sn',img='q')
                if dlg=='n': return
            self.Modifica = 0
            #
            nombre = Entra_dlg(self,'','Nombre de la ventana nueva:')
            if nombre==-1: return
            
            propgen = []    # Propiedades Generales de la ventana
            propgen.append('Ventana '+nombre)  # Descripción
            propgen.append('')                 # Nombre Ventana Padre
            propgen.append('')                 # Icono Ventana
            propgen.append('')                 # Titulo de la ventana
            propgen.append('800')              # Tamaño X
            propgen.append('600')              # Tamaño Y
            propgen.append('c')                # Pos X inicial (c=Centro)
            propgen.append('c')                # Pos Y inicial (c=Centro)
            propgen.append('')                 # Nombre de la tabla Asociada
            propgen.append('')                 # Campo que contiene Clave Tabla
            propgen.append('')                 # Acción Cargar Ventana
            propgen.append('')                 # Acción Despues de Leer
            propgen.append('')                 # Boton a Ejecutar con FIN
            data={}
            data[self.NOMBRE_ROOT] = propgen   
            self.arbol.AddRoot(self.NOMBRE_ROOT)         
            #
            dicc = bsddb.btopen(self.fileName)
            datoswin = copia_rg(propgen)
            datoswin.append([]) # Ningun elemento Hijo al empezar
            dicc[nombre] = pickle.dumps(datoswin)
            dicc.close()
            #
            self.Ejecuta_Accion('a_carga_wins')
            self._ct['L1'].Sel_Item(nombre)


        elif accion=='a_borra':
            """ Borrar una tabla """
            sele = self._ct['L1'].GetValue()
            if sele==None:
                Men('Debe seleccionar la ventana a borrar')
                return -1
            dlg = Men('¿Está seguro de borrar la ventana '+sele+'?','sn',img='q')
            if dlg=='n': return -1
            dicc = bsddb.btopen(self.fileName)
            del dicc[sele]
            dicc.close()
            Men('Ventana Borrada')
            self.Ejecuta_Accion('a_carga_wins')
            
        elif accion=='a_graba_cambio':
            arbol = self.arbol
            data = self.data
            grid = self._ct['G1']
            fila = grid.GetNRow() - 1
            nodo = arbol.GetSelection()
            if nodo.IsOk():
                idnodo = arbol.GetItemText(nodo)
                self.data[idnodo][fila] = grid.GetValue(fila,1)
                self.Modifica = 1
            
        elif accion=='a_graba':
            """ Grabar los datos de la ventana actual """
            
            win = self._ct['L1'].GetValue()
            if win==None:
                Men('No hay seleccionada ventana')
                return -1
            datos = self.Arbol_a_Datos()
            #
            dicc = bsddb.btopen(self.fileName)
            dicc[win]=pickle.dumps(datos)
            dicc.close()
            #
            self.Modifica = 0
            Men('Ventana Guardada',img='i')
            #self.Ejecuta_Accion('a_carga_wins')
        elif accion=='a_ejecuta':
            sele = self._ct['L1'].GetValue()
            if sele==None:
                Men('Debe seleccionar la ventana a ejecutar')
                return -1
            wins = bsddb.btopen(self.fileName)
            datos = pickle.loads(wins[sele])
            wins.close()

            codigo = "#!/usr/bin/env python    "+"\n"
            codigo += "# -*- coding: iso-8859-1 -*-"+"\n"
            codigo += "import wx"+"\n"
            codigo += "import OC"+"\n"
            codigo += "from OC.Funciones import *"+"\n"

            codigo += "class "+sele+"(OC.Ventana):"+"\n"
            codigo += "    def __init__(self):"+"\n"
            codigo += "        OC.Ventana.__init__(self, None,'"+datos[3]+"',tam=("+datos[4]+","+datos[5]+"))"+"\n"
            ##
            codigo += "        ls_campos = "+str(datos[-1])+"\n"
            #
            codigo += "        self.init_ctrls(ls_campos)"+"\n"
            
                
            codigo += "win = "+sele+"()"
            debug(codigo)
            exec(codigo)
            return 0
        
        elif accion=='a_detalle_entradas':
            import dl_entrys
            dlg = dl_entrys.Detalle_Entrys(self)
            #dlg.ShowModal()
            print dlg.GetValue()
            dlg.Destroy()
            return 0  
                
        else:
            return -999    
            
            

#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App(False)
    ventana = Manage_Win()
    ventana.Show()
    app.MainLoop()

