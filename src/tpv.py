#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx
import OC
import os
from OC.Funciones import *

from global_var import DIR_IMG
from global_var import DIR_DATA


class tpv(OC.Ventana):
    """ Ficha para manejar las ventas de la aplicaci�n """

    def __init__(self,padre=None):

        OC.Ventana.__init__(self, padre,'TPV',tam=(940,660))
        #
        ls_campos = []

        p1 = ['PANEL','P1',0,0,600,200,'','2','',[]]

        # LISTA DE ARTICULOS DISPONIBLES
        cols=[['Codigo','%'],['Nombre','l'],['PVP','2']]
        ls = ['LIST','L1',120,10,470,140,cols,'','','','','','a_pon_arti','']
        p1[-1].append(ls)

        ent = ['ENTRYS','ENT_P1','25','50','','',[]]
        ent[-1].append(['BUSCA','[Busca','160','155','20','l','100','','','','a_filtra','','','',''])
        p1[-1].append(ent)

        ## ----
        p2 = ['PANEL','P2',0,205,600,290,'','0','',[]]

        ent = ['ENTRYS','ENG','25','50','','',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        ent[-1].append(['IDX','N�Venta','10','245','9','%','6','','','','a_LEE_RG','','','',''])
        ent[-1].append(['AV_TN','Tecn','20','25','4','%','3','','','','','','','',''])
        ent[-1].append(['AV_CL','Cliente','80','25','7','%','6','','','','a_pon_cliente','clientes,cl_ls','','',''])
        ent[-1].append(['CL_DENO','Nombre Cliente','-1','','30','l','100','n','','','','','','',''])
        ent[-1].append(['AV_FEC','Fecha','-1','','9','d','10','','','','','','','',''])
        ent[-1].append(['AV_TTT','[Total','485','210','7','2','100','n','','','','','','',''])
        ent[-1].append(['AV_COB','[Cobrado','485','235','7','2','100','n','','','','','','',''])
        ent[-1].append(['AV_PTE','[Pendiente','485','260','7','2','100','n','','','','','','',''])

        p2[-1].append(ent)

        p2[-1].append(['CHECK','AV_PTJ','280','240','2','100','Tarjeta Credito','0','','',''])

        # GRID CON LA VENTA ACTUAL
        #---
        cols = []
        cols.append(['Codigo',7,'%',6,'','','','','a_completa_linea','','','','',''])
        cols.append(['Nombre',37,'l',0,'n','n','cache(articulos,0,AR_DENO)','','','','','','',''])
        cols.append(['Uds',4,'i',0,'n','','','','','','','','',''])
        cols.append(['Precio',7,'2',0,'','','','','a_pon_ttt','','','','',''])
        #
        p2[-1].append(['GRID','AV_LNA','',5,60,590,22,5,cols,0,'',''])


        # BOTONES SOBRE LISTA
        btn=[]
        btn.append(['B1',150,225,50,'c_mas.png','','a_suma_arti','A�adir Art�culo',''])
        btn.append(['B2',210,225,50,'c_menos.png','','a_resta_arti','Eliminar Art�culo',''])
        p2[-1].append(['BUTTONS','BID',50,'','',btn])
        #
        btn=[]
        btn.append(['B3',560,255,37,'gastos.png','','a_cobra_pte','Cobrar Pendiente',''])
        p2[-1].append(['BUTTONS','BID2',32,'','',btn])
        #
        ls_campos.append(p2)
        ls_campos.append(p1)

        #- Logo
        plogo = ['PANEL','PLOGO',600,0,350,200,'','2','',[]]
        ls_campos.append(plogo)

        #- Ptes Pago
        pptes = ['PANEL','PPTES',600,205,350,290,'','1','',[]]
        cols = [['N� Venta','l'],['Fecha','d'],['Importe','2'],['Pte ','l']]
        ls = ['LIST','LP',5,25,300,100,cols,'','','','','','a_carga_rgp','']
        pptes[-1].append(ls)
        #
        cols = [['N� Cobro','l'],['Fecha','d'],['Importe','2']]
        ls = ['LIST','LC',5,175,300,100,cols,'','','','','','','']
        pptes[-1].append(ls)
        #
        btn=[]
        btn.append(['BTBV',310,30,25,'','X','a_borra_ventap','Borrar Venta',''])
        btn.append(['BTBC',310,180,25,'','X','a_borra_cobro','Borrar Cobro',''])
        pptes[-1].append(['BUTTONS','BID',25,'','',btn])
        #
        ls_campos.append(pptes)



        #P3 - Botones de la Ventana
        p3 = ['PANEL','P3',602,500,335,158,'','2','',[]]
        btn=[]
        btn.append(['BTI',5,10,65,'left.png','','a_PREV','Registro Anterior',''])
        btn.append(['BTD',85,10,65,'right.png','','a_NEXT','Registro Siguiente',''])
        btn.append(['BTG',5,60,65,'save.png','','a_GRABA:a_antes_grabar,n|a_desp_grabar','Grabar Venta',''])
        btn.append(['BTB',85,60,65,'delete.png','','a_BORRA:a_antes_borrar','Borrar Venta',''])
        btn.append(['BTN',5,110,65,'new.png','','a_NUEVO:LC,LP,CL_DENO','Nueva Venta',''])
        btn.append(['BTS',85,110,65,'select.png','','a_INFO:alb-venta,av_ls,LS','',''])
        btn.append(['B8',180,60,95,'exit.png','Salir','a_SALIR','',''])
        p3[-1].append(['BUTTONS','BID',45,'','',btn])

        ls_campos.append(p3)
        
        #P4 - Lista de Selecci�n
        p4 = ['PANEL','P4',0,500,600,160,'','','',[]]
        cols = [['Codigo','l'],['Cliente','l'],['Nombre Cliente','l'],['Fecha','d'],['Importe','2'],['Pendiente','l']]
        ls = ['LIST','LS',0,0,-1,-1,cols,'','','','','','a_carga_rg','']
        p4[-1].append(ls)

        ls_campos.append(p4)

        self._idx = 'IDX'
        self._filedb = 'alb-venta'
        self._accini='a_cambia_tipo'        # Acci�n al cargar la ventana
        self._accleer = ''       # Acci�n despues de leer registro
        self._btfin = 'BTG'     # Nombre del boton a ejecutar cuando pulse boton FIN
        #
        self.init_ctrls(ls_campos)

        #

        #-- RADIO BUTTON TIPO ARTICULO
        radio=wx.RadioBox(self._ct['P1'],-1,"Tipo Articulo",(10,10),wx.DefaultSize,
            ['Servicio','Producto'],1,wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX,self.OnRadio,radio)
        self._radio = radio

        self._ct['BUSCA'].Set_ADK('a_filtra_ar')
        self._ct['AV_PTJ'].Enable(0)

        if self._accini<>'': self.Ejecuta_Accion(self._accini)
        self.Modifica = 0

        #-- LOGO
        img = wx.Image(DIR_IMG+'/logo.jpg',wx.BITMAP_TYPE_ANY)
        img = img.Scale(340,240)
        sb = wx.StaticBitmap(self._ct['PLOGO'],-1,wx.Bitmap(img))
        
        #-- Al final, pq debe estar creado el panel
        label = wx.StaticText(self._ct['PPTES'],label='Ventas Ptes Pago del Cliente actual')
        label.SetPosition((50,0))
        #--
        label = wx.StaticText(self._ct['PPTES'],label='Cobros de la Venta Actual')
        label.SetPosition((100,150))

    #
    #-- Acci�n al seleccionar el radiobutton
    #
    def OnRadio(self,event):
        self.Ejecuta_Accion('a_cambia_tipo',event.GetEventObject())


    #
    #-- Acciones a ejecutar
    #
    def Ejecuta_Accion(self,accion,obj=None):
        try:
            """ Acciones a ejecutar """
            # Probamos primero si es una accion estandar
            std = OC.Ventana.Ejecuta_Accion(self, accion,obj)
            ok,val = std
            
            # Comprobar el valor devuelto por si hay que hacer algo
            # Ya se ejecut� la accion. No continuar con la accion normal
            if ok<>0:
                return std

            pb = self
            ct = pb._ct
            cta = pb._cta
            if obj<>None: cta=obj

            global ls_articulos

            if accion=='a_carga_rg':
                cod=self._ct['LS'].GetValue()
                if cod<>None: self._ct[self._idx].SetValue(cod)
                self.Modifica = 0
                
            if accion=='a_carga_rgp':
                cod=self._ct['LP'].GetValue()
                if cod<>None: self._ct[self._idx].SetValue(cod)
                self.Modifica = 0
                

            if accion=='a_cambia_tipo':
                tipo = self._radio.GetSelection()
                preg = []
                if tipo==0: preg.append(['AR_TIPO','=','S'])
                elif tipo==1: preg.append(['AR_TIPO','=','A'])
                lsar = select('articulos','0 AR_DENO AR_PVP',preg,'AR_DENO')
                ls_articulos = lsar
                ct['L1'].SetValue(lsar)
                ct['BUSCA'].SetValue('')
                ct['BUSCA'].SetFocus()

            elif accion=='a_pon_cliente':
                cdcl = cta.GetValue()
                if cdcl=='':
                    ct['CL_DENO'].SetValue('')
                else:
                    cli = lee('clientes',cdcl)
                    if cli==1:
                        Men('No se pudo leer el cliente '+cdcl)
                        return -1
                    ct['CL_DENO'].SetValue(cli['CL_DENO'])

                pb.Ejecuta_Accion('a_pon_datos_cliente',ct['AV_CL'])

                ptes = ct['LP'].GetValue(fmt='L')
                #if ptes<>[]: Men('El cliente tiene pagos pendientes.')
                    
            elif accion=='a_pon_datos_cliente':
                cdcl = cta.GetValue()
                cdav = ct['IDX'].GetValue()
                #- Vemos si tiene ventas pendientes
                ls = []
                if cdcl<>'':
                    rs = select('alb-venta','0 AV_PTE AV_FEC AV_TTT',[['AV_CL','=',cdcl],['AV_PTE','>','0']])
                    if rs <> []:
                        for ln in rs:
                            ls.append([ln[0],ln[2],ln[3],ln[1]])
                ct['LP'].SetValue(ls)
                
                if cdav<>'':
                    #- Mostramos la lista de cobros de la venta
                    ls = []
                    idx = ct['IDX'].GetValue()
                    rs = select('cobros','0 CB_FEC CB_IMPO',[['CB_CDAV','=',idx]])
                    if rs <> []:
                        for ln in rs:
                            ls.append([ln[0],ln[1],ln[2]])
                    ct['LC'].SetValue(ls)
                    

            elif accion=='a_pon_arti':
                sele = ct['L1'].GetValue(fmt='l')
                venta = ct['AV_LNA'].GetData()
                sele = copia_rg(sele)
                sele.insert(2,'1')
                venta.append(sele)
                ct['AV_LNA'].SetData(venta)
                self.Ejecuta_Accion('a_pon_ttt')

            elif accion=='a_completa_linea':
                venta = ct['AV_LNA'].GetData()
                fila,col = ct['AV_LNA'].GetCursor()
                #fila = fila-1   # -1 pq desp. editar est� en la siguiente
                #       ... esto era pq solo hab�a una columna editable ...
                cdar=''
                if fila>=0 and venta<>[]: cdar = venta[fila][0]
                if cdar<>'':
                    ar = lee('articulos',cdar)
                    if ar<>1:
                        venta[fila][1]=ar['AR_DENO']
                        venta[fila][2]='1'
                        venta[fila][3]=ar['AR_PVP']
                    else:
                        Men('No existe el art�culo '+cdar)
                        ##venta = venta[:-1]
                        ##ct['AV_LNA'].SetCursor(0,0)

                    ct['AV_LNA'].SetData(venta)
                    self.Ejecuta_Accion('a_pon_ttt')

            elif accion=='a_suma_arti':
                venta = ct['AV_LNA'].GetData()
                fl = ct['AV_LNA'].GetNRow()
                if fl>=len(venta): return
                venta[fl][2] += 1
                ct['AV_LNA'].SetData(venta)
                self.Ejecuta_Accion('a_pon_ttt')


            elif accion=='a_resta_arti':
                venta = ct['AV_LNA'].GetData()
                fl = ct['AV_LNA'].GetNRow()
                if fl>=len(venta): return
                venta[fl][2] -= 1
                if venta[fl][2]<=0:
                    if fl < len(venta):
                        del venta[fl]
                ct['AV_LNA'].SetData(venta)
                self.Ejecuta_Accion('a_pon_ttt')

            elif accion=='a_pon_ttt':
                venta = ct['AV_LNA'].GetData()
                ttt=0
                for ln in venta:
                    ttt += ln[2]*ln[3]
                ct['AV_TTT'].SetValue(ttt)

            elif accion=='a_filtra_ar':
                lsar = ls_articulos
                busca = ct['BUSCA'].GetValue()
                busca = busca.upper()
                resul=[]
                for ln in lsar:
                    deno = ln[1].upper()
                    if busca in deno: resul.append(ln)
                ct['L1'].SetValue(resul)

            elif accion=='a_antes_grabar':
                fec = ct['AV_FEC'].GetValue()
                if fec==None: ct['AV_FEC'].SetValue(Fecha())
                #-
                if ct['AV_LNA'].GetValue() == []:
                    Men('No ha indicado ning�n art�culo')
                    return -1
                #
                if ct['AV_CL'].GetValue() == '':
                    Men('Debe indicar cliente')
                    return -1
                #
                ttt=ct['AV_TTT'].GetValue()
                cob=ct['AV_COB'].GetValue()
                ct['AV_PTE'].SetValue(ttt-cob)
                #
                
            elif accion=='a_antes_borrar':
                lscb = ct['LC'].GetValue('L')
                if lscb<>[]:
                    Men('La venta tiene cobros asignados.\nDebe borrarlos antes de borrar la venta.')
                    return -1

            elif accion=='a_graba_venta':
                signo = self._signo
                rg = self._rg       # Se quedar�n las modificaciones en rg
                #
                for ln in rg['AV_LNA']:
                    cdar,uds = ln[:2]
                    ar = lee('articulos',cdar)
                    if ar==1: continue
                    ar['AR_STK'] -= uds*signo
                    p_actu('articulos',cdar,ar)
                #
                self._rg = rg  

            elif accion=='a_desp_grabar':
                cob = self._ct['AV_COB'].GetValue()
                if cob==0:  # Si es una venta nueva, mostramos el dialogo de cobro
                    pb.Ejecuta_Accion('a_cobra_pte')
                    ##ct['IDX'].SetValue(ct['IDX'].GetValue()) => Lo ejecuta la accion anterior
                

            elif accion=='a_cobra_pte':
                cdav = self._ct['IDX'].GetValue()
                if cdav=='' or cdav=='.' or self.Modifica==1: 
                    Men('Debe guardar la venta antes de cobrar')
                    return 1
                #
                pte = self._ct['AV_PTE'].GetValue()
                cob = self._ct['AV_COB'].GetValue()
                ttt = self._ct['AV_TTT'].GetValue()
                if pte==0 and cob==ttt:
                    Men('Esta venta no tiene importe pendiente.')
                    return 1
                #
                res = self.Muestra_Dlg_Pago()
                if res==-1: return 
                importe,tarj = res
                
                if tarj: importe = pte
                if importe==0:
                    Men('No se puede generar cobro con importe cero')
                    return
                else:
                    cod = self.Crea_Cobro(cdav,importe,tarj)
                    if cod==1:  Men('No se pudo crear el cobro.')

                ct['IDX'].SetValue(ct['IDX'].GetValue())
                    
            #
            #-- Borra el cobro seleccionado de la venta actual
            #
            elif accion=='a_borra_cobro':
                cdav = self._ct['IDX'].GetValue()
                cdcb = ct['LC'].GetValue()
                if cdcb==None:
                    Men('No ha seleccionado ning�n cobro para borrar')
                else:
                    dlg=Men('�Est� seguro de borrar el cobro '+cdcb+'?','sn','q')
                    if dlg=='n': return 0  
                    
                    ok = self.Borra_Cobro(cdav,cdcb)
                    if ok<>None:
                        #Men('Cobro '+cdcb+' borrado')
                        ct['IDX'].SetValue(ct['IDX'].GetValue())  
                    else:
                        Men('No se pudo borrar el cobro.')

            #
            #-- Borra el registro de venta pendiente seleccionado
            #
            elif accion=='a_borra_ventap':
                cdav = ct['LP'].GetValue()
                if cdav==None:
                    Men('No ha seleccionado ninguna venta pendiente para borrar')
                else:
                    dlg=Men('�Est� seguro de borrar la venta '+cdav+'?','sn','q')
                    if dlg=='n': return 0  
                    
                    ok=borra_dicc('alb-venta.db',cdav,DIR_DATA)
                    if ok<>None:
                        #Men('Venta '+cdav+' borrada')
                        pb.Ejecuta_Accion('a_pon_datos_cliente',ct['AV_CL'])
            
            
        except:
            Men(accion+'\n'+Busca_Error())


        return 0 # No se ejecut� ninguna accion o todo correcto

    #
    #- Muestra el dialogo de cobro, devuelve el importe y si es con tarjeta
    #
    def Muestra_Dlg_Pago(self):
 
        ls_campos=[]
        ent = ['ENTRYS','COBRO','30','50','','RF/12',[]]
        #enf[-1].append(['ID','Etiq','X','Y','Ancho','Fmt','lmax','edi','FCal','Sobre','ADE','Dlg','Tip','CPAN','Style'])
        ent[-1].append(['PAGAR',':A Pagar','60','10','10','2','6','','','','','','','',''])
        ent[-1].append(['ENTREGA',':Entrega','60','60','10','2','6','','','','a_pon_cambio','','','',''])
        ent[-1].append(['CAMBIO',':Cambio','60','110','10','2','6','','','','','','','',''])
        ent[-1].append(['NADA','xxx','660','1100','1','l','6','','','','','','','',''])

        ls_campos.append(ent)
        ls_campos.append(['CHECK','AV_PTJ','60','145','2','100','Tarjeta Credito','0','','',''])

        dl = OC.Dialogo(self,'Cobrar',ls_campos,(620,620))
        ttt = self._ct['AV_TTT'].GetValue()
        pagado = self._ct['AV_COB'].GetValue()
        dl.SetValue('PAGAR',ttt-pagado)
        #dl.SetValue('ENTREGA',ttt-pagado)
        res = dl.res()
        if res==None: return -1
        pagar,entrega,cambio,nada,tarjeta = res
        
        if entrega > pagar:
            entrega = pagar
        
        return (entrega,tarjeta)
    
    #
    #-- Crea un cobro con los datos pasados por argumentos
    #
    def Crea_Cobro(self,cdav,importe,tarj):
       
        rg = rg_vacio('cobros')
        idx = u_libre('cobros')
        rg['CB_DENO']='Cobro de la venta '+cdav
        rg['CB_FEC']=Fecha()
        rg['CB_IMPO']=importe
        rg['CB_CDAV']=cdav
        rg['CB_TARJ']=tarj
       
        av=lee('alb-venta',cdav)
        if av==1: return 1
        av['AV_COB']+=importe
        av['AV_PTE']-=importe
        if tarj: av['AV_PTJ']=1  # Si uno de los cobros es con tarjerta, ponemos la venta con tarjeta
        
        p_actu('cobros',idx,rg) 
        p_actu('alb-venta',cdav,av) 
        
        return idx
    
    #
    #
    #
    def Borra_Cobro(self,cdav,cdcb):
        rg = lee('cobros',cdcb)
        if rg==1:
            Men('No se pudo leer el cobro '+cdcb)
            return None
        importe = rg['CB_IMPO']
        
        ok=borra_dicc('cobros.db',cdcb,DIR_DATA)
        if ok==None: return None
        
        av=lee('alb-venta',cdav)
        if av==1: return 1
        av['AV_COB']-=importe
        av['AV_PTE']+=importe
        
        p_actu('alb-venta',cdav,av) 
        return 1



#############################################################
#
#
#
#
##############################################################
if __name__ == "__main__":
    app = wx.App(False)
    ventana = tpv()
    ventana.Show()
    app.MainLoop()
