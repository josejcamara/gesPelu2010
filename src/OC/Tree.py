#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx

class Tree(wx.TreeCtrl):
    """ Clase Arbol """
    def __init__(self,pb,parent,name,raiz='Raiz',data=[]):
        self.__pb = pb
        self.__data = data
        
        wx.TreeCtrl.__init__(self,parent,name=name)
        self.SetSize(parent.GetSize())
        root= self.AddRoot(raiz)
        self.AddTreeNodes(root, ls_campos)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.onClick,self)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.onDClick,self)
        
        
    def AddTreeNodes(self,parentItem,items):
        for item in items:
            tipo = item[0]
            deno = tipo+ ' '
            hijos = item[-1]
            #
            if tipo in ('PANEL','GRID','LIST'):
                deno += item[1]
                if tipo in ('GRID','LIST'): hijos=[]
            elif tipo in ('ENTRYS','BUTTONS'):
                deno += hijos[0][0]
            else:
                hijos = []
            #
            nodo = self.AppendItem(parentItem,deno)
            if hijos<>[]:
                self.AddTreeNodes(nodo, hijos)
   
    #
    #-- Al seleccionar un elemento
    #
    def onClick(self,evt):
        item = evt.GetItem()
        raiz = self.RootItem
        data = self.__data
        #
        if item == raiz:
            print 'Propiedades generales de la ventana'
        else:
            ruta=[self.GetItemText(item)]
            padre = self.GetItemParent(item)
            while padre <> raiz:
                ruta.insert(0,self.GetItemText(padre))
                padre = self.GetItemParent(padre)
            
            #- Buscamos los datos del nodo seleccionado
            info = []
            for nodo in ruta:
                tipo,nombre = nodo.split(' ')
                for elem in data:
                    if tipo<>elem[0]: continue
                    if tipo in ('PANEL','GRID','LIST'):
                        if nombre<>elem[1]: continue
                    elif tipo in ('ENTRYS','BUTTONS'):
                        if nombre<>elem[-1][0][0]: continue
                    else:
                        continue
                    
                    info = elem
                    data = elem[-1]
                    break
            print '***************************'
            if tipo=='PANEL': info = info[:-1]
            print info
            print '***************************'
            #
            
    
                 
    #
    #-- Al hacer doble clik sobre un elemento
    #
    def onDClick(self,evt):
        item = self.GetItemText(evt.GetItem())
        print item
   

#############################################
#
#
#############################################
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = wx.Frame(None,title="Prueba de la Clase Grid")
    frame.SetSize((800,600))
    frame.CentreOnScreen()
    #
    #############################################################
    ls_campos=[]
    #            
    p1 = ['PANEL','P1',0,0,600,400,'B-236:44:26/RF',[]]
    hijosp1=[]
    hijosp1.append(['E1','Código',10,15,'%',6,7,'','','','','ar_ls','codigo delcliente','clientes',''])
    hijosp1.append(['E2','Nombre del Cliente',-1,0,'l',100,25,'','','','','','','',''])
    hijosp1.append(['E3','Direccion',-1,0,'l',100,25,'','','','','','Domicilio','',''])
    hijosp1.append(['E4','Población',-1,0,'l',100,25,'','','','','','Pueblo','',''])
    hijosp1.append(['E5','Provincia',-1,0,'l',100,15,'','','','','','Ciudad','',''])
    hijosp1.append(['E6','CPostal',-1,0,'l',5,15,'n','','','','','Código Postal','',''])
    p1[-1].append(['ENTRYS',22,50,'F-255:255:0','B-0:0:0/F-255:255:255',hijosp1])
    #
    cols = []
    cols.append(['Articulo','%',6,7,'','','','a_lee_ar','sel-ar,ar_ls','Código','articulos',''])
    cols.append(['Nombre Articulo','l',0,12,'','','a_pon_deno','','','Nombre','',''])
    cols.append(['Fecha','d',0,10,'','','Fecha()','','','Fecha','',''])
    cols.append(['Precio','2',0,10,'','','','','','Precio ','',''])
    cols.append(['No\nEditable','l',0,10,'n','','','','','Nada','',''])
    
    p1[-1].append(['GRID','G1',10,150,500,5,22,cols,1,[],'',''])
    
    #
    #
    p3 = ['PANEL','P3',605,100,190,400,'B-36:144:26/RF',[]]
    # Button(None,p1,'B1',(100,100),(60,40),'','Abrir','abrir','Abrir Archivo')
    lsbtn = []
    lsbtn.append(['B1',(10,10),40,'','Bt1','a_boton1','Ayuda Boton1'])
    lsbtn.append(['B2',(60,10),40,'','Bt2','a_boton2','Ayuda Boton2'])
    lsbtn.append(['B3',(10,60),40,'','Bt3','a_boton3','Ayuda Boton3'])
    lsbtn.append(['B4',(60,60),40,'','Bt4','a_boton4','Ayuda Boton4'])
    lsbtn.append(['B5',(10,110),40,'','Bt5','a_boton5','Ayuda Boton5'])
    p3[-1].append(['BUTTONS',40,'','',lsbtn])
                   
    #
    # ['LISTA',nombre, xini, yini, tamanox, tamanoy, cols, 
    #        acc_click, acc_dclick]
    p4 = ['PANEL','P4',0,410,600,400,'B-236:144:126/RF',[]]
    p4[-1].append(['LIST','L1',5,5,500,100,[['Código','l'],['Nombre','l'],['Importe','2']],"al_click","al_dclick"])
    
    # PANELES: ['PANEL',nombre, xini, yini, tamanox, tamanoy,color,lista_hijos]
    ls_campos.append(p1)
    ls_campos.append(p3)
    ls_campos.append(p4)
    ####################################################


    #arbol.AddTreeNodes(raiz, ls_campos)
    #
    p1 = wx.Panel(name='PANEL1', parent=frame,pos=(0,100),size=(150,400))
    p2 = wx.Panel(name='PANEL2', parent=frame,pos=(150,0),size=(500,400))
    arbol = Tree(None,p1,'Tree1','Ventana Clientes',ls_campos)
    raiz = arbol.RootItem
    
    #
    frame.Show()
    app.MainLoop()
