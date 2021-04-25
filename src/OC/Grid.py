#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import wx
import wx.grid as wx_grid
import Funciones
import Entry

class Grid():

    def __init__(self,pb,parent,name,pos,ancho,hrow=22,nrows=5,cols=[],rlsize=0,rlabels=[],prop='',titu=''):
        grid = wx_grid.Grid(name=name,parent=parent)
        ncols = len(cols)
        #
        grid.CreateGrid(nrows,ncols)
        grid.SetPosition(pos)
        grid.SetColMinimalAcceptableWidth(0)
        #
        gancho = 0
        gancho += rlsize*10
        fmts,edi,graba=[],[],[]
        anchos,fcals = [],[]
        dlcols = []
        for c in range(ncols):
            titc,wcol,fmt,lmax,edit,grab,fcal,sobre,ade = cols[c][:9]
            dlsel,totales,tip,cpan,style = cols[c][9:]

            fmts.append(fmt)
            anchos.append(wcol)
            edi.append(edit)
            graba.append(grab)
            fcals.append(fcal)
            dlcols.append(dlsel)
            #
            attr = wx_grid.GridCellAttr()
            if edit in ('n','i'):
                attr.SetReadOnly(True)
                attr.SetBackgroundColour(wx.Colour(235,235,235))
                if edit=='i': wcol=0

            attr.SetEditor(OC_CellEditor(self,pb,parent,fmt,lmax,dlsel,edit,fcal,sobre,ade,cpan))
            grid.SetColAttr(c,attr)

            grid.SetColLabelValue(c,titc)
            grid.SetColSize(c,wcol*10)
            #
            gancho += wcol*10.4

        #- Ajustamos el tamaño del grid si es menor
        gancho = int(gancho)
        hclabel = grid.GetColLabelSize()    # Alto de la fila de títulos
        size = (ancho,nrows*(hrow) + hclabel+5)
        grid.SetDefaultRowSize(hrow)
        #
        grid.SetSize(size)
        if rlsize==0: rlsize=1
        else: rlsize = rlsize*10
        grid.SetRowLabelSize(rlsize)    # Row Label Size
        nlabels = len(rlabels)
        for nr in range(nlabels):
            rlabel = rlabels[nr]
            if nr>=nrows: grid.AppendRows()
            grid.SetRowLabelValue(nr,rlabel)

        #- TITULO
        if titu<>'':
            titux=pos[0]+gancho/2
            tituy=pos[1]-15
            titu = wx.StaticText(parent,-1,titu,(titux,tituy))

        #- EVENTOS
        grid.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.onSelectCell)
        grid.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)


        #
        self.Parent = parent
        self._name = name
        self.__pb = pb
        self.__grid = grid
        self.__fmts = fmts  # Lista de Formatos de las columnas
        self.__edi = edi    # Lista indicando por columna, si es editable
        self.__graba = graba  # Lista indicando por columna, si es grabable
        self.__hrow = hrow      # Alto de la fila
        self.__anchos = anchos
        self.__fcals = fcals    # Formula de Calculo
        self.__dlcols = dlcols  # Dialogos de Seleccion
        self.__rlabels = rlabels    # Titulo de las filas (cuando fijas)
        self.__titu = titu      # Titulo del Grid
        #
        self.__dlcells = {} # Diccionario dialogos seleccion por fila,col
        self.__fmtcells= {} # Diccionario de formatos por celda

    #
    #-- Devuelve la fila y la columna en la que estamos
    #
    def GetCursor(self):
        grid = self.__grid
        col,fil = grid.GridCursorCol, grid.GetGridCursorRow()
        return (fil,col)

    #
    #-- Pone el foco en una celda del grid
    #
    def SetCursor(self,fil,col):
        grid = self.__grid
        grid.SetGridCursor(fil,col)
        #grid.ShowCellEditControl()
        grid.EnableCellEditControl()

    #
    #
    #
    def SetFocus(self,fila=0,col=0):
        grid = self #.__grid
        if fila<>-1 and col<>-1:
            grid.SetCursor(fila,col)
        else:
            grid.SetFocus()


    #
    #-- Mueve el cursor a la proxima celda editable
    #
    def Next_Cell(self):
        grid = self.__grid
        col,fil = grid.GridCursorCol, grid.GetGridCursorRow()
        ucol = grid.NumberCols -1
        ufil = grid.NumberRows -1

        if fil==ufil and col==ucol:
            if not (self.__rlabels in ([],'')): # Estamos al final del grid
                self.__pb.Next_Ctrl(self)       #  con unas filas fijas
                return


        ca = col    # Columna Actual
        col = (col+1)%len(self.__edi)
        while self.__edi[col] in ['n','i']:
            col = (col+1)%len(self.__edi)
            if col == ca: break

        if col<=ca: fil+=1
        if fil>ufil : grid.AppendRows(1)
        grid.SetGridCursor(fil,col)
        ##grid.EnableCellEditControl()


    #
    #-- Mueve el cursor a la anterior celda editable
    #
    def Prev_Cell(self):
        grid = self.__grid
        col,fil = grid.GridCursorCol, grid.GetGridCursorRow()
        ucol = grid.NumberCols -1
        #ufil = self.NumberRows -1

        ca = col
        if col==0 and fil==0:
            self.__pb.Prev_Ctrl(self)
            return      # Salimos del grid
        elif col==0:
            fil=fil-1
            if fil<0: fil=0
            col=ucol
            while self.__edi[col] in ['n','i']:
                col = (col-1)%len(self.__edi)
                if col == ca: break

        else:
            col = (col-1)%len(self.__edi)
            while self.__edi[col] in ['n','i']:
                col = (col-1)%len(self.__edi)
                if col == ca: break
            if col>=ca:
                fil-=1
        grid.SetGridCursor(fil,col)
        ##grid.EnableCellEditControl()


    #
    #-- Evento al posicionarse sobre una celda
    #
    def onSelectCell(self,event):
        col = event.Col
        row = event.Row

        event.Skip()


    #
    #-- Asigna los títulos por fila al grid
    #
    def SetTituxRows(self,titulos,ancho):
        """ Asigna los títulos por fila al grid"""
        pass
    #
    #
    #
    def GetTituxSize(self):
        return self.__grid.GetColLabelSize()
    #
    #-- Asigna propiedades al grid
    #
    def SetProperties(self,prop):
        """ Asigna propiedades al grid """
        pass

    #
    #-- Pone un estilo a las celdas de datos del grid
    #
    def SetDataStyle(self,style):
        """ Pone un estilo a las celdas de datos del grid """
        pass


    #
    #
    #
    def SetData(self,value):
        grid = self.__grid
        lsfmt = self.__fmts
        grid.ClearGrid()
        nf=0
        for lnf in value:
            if nf >= grid.GetNumberRows(): grid.AppendRows()
            for nc in range(len(lnf)):
                valor = Funciones.Fmt_a_Str(lnf[nc],lsfmt[nc])
                grid.SetCellValue(nf,nc,valor)
            #
            nf+=1
        self.__pb.Modifica=1

    #
    #
    #
    def SetValue(self,value,fila=-1,col=-1):
        grid = self.__grid
        lsfmt = self.__fmts
        grabables = self.__graba
        fcal = self.__fcals

        self.__pb.Modifica=1

        if fila<>-1 and col<>-1:
            value = Funciones.Fmt_a_Str(value,lsfmt[col])
            grid.SetCellValue(fila,col,value)
        else:
            grid.ClearGrid()
            nf=0
            for lnv in value:   # Filas
                quita=0
                if nf >= grid.GetNumberRows(): grid.AppendRows()
                for nc in range(len(lsfmt)):
                    if grabables[nc]=='n': quita+=1
                    if fcal[nc]<>'':
                        formula = fcal[nc]
                        if formula[0]=='<' and formula[-1]=='>':  # Valor Columna Anterior
                            valor = lnv[int(xxx[1])]
                        else:
                            if formula[:6]=='cache(':   # Valor de Caché
                                xxx = formula.split(',')
                                xxx[1] = lnv[int(xxx[1])]
                                formula = ','.join(xxx)
                            #
                            valor = self.__pb.Valor_FC(formula)

                    else:
                        valor = Funciones.Fmt_a_Str(lnv[nc-quita],lsfmt[nc])
                    grid.SetCellValue(nf,nc,valor)
                    #
                    nc+=1
                #
                nf+=1

    #
    #- Devuelve el conjunto de datos del grid
    #
    def GetData(self):
        grid = self.__grid
        v=[]

        nfilas = grid.GetNumberRows()
        ncols = len(self.__fmts)
        for nf in range(nfilas):
            lnv = []
            for nc in range(ncols):
                value = grid.GetCellValue(nf, nc)
                cfmt = self.GetFmt(nc,nf)
                if cfmt in ('l','%'): value = value.encode('latin-1')
                elif cfmt =='i':
                    if value=='': value=0
                    else: value = int(value)
                elif cfmt == 'd':
                    if value=='': value=None
                    else: value = Funciones.Fecha_aNum(value)
                elif cfmt in ('0','1','2','3','4','5','6','7','8','9'):
                    if value=='': value=0.0
                    else: value = float(value)
                lnv.append(value)

            #- Si no hay filas fijas, pasamos las filas con 1º colum vacia
            fmt1 = self.__fmts[0]
            if self.__rlabels in ([],''):
                if lnv[0]=='' and fmt1 in ('l','%'): continue
                if lnv[0]==None and fmt1 == 'd': continue
                if lnv[0]==0 and fmt1 in ('i','0','1','2','3','4','5','6','7','8','9'): continue
            #
            v.append(lnv)

        return v


    #
    #
    #
    def GetValue(self,fila=-1,col=-1):
        data = self.GetData()
        grabable = self.__graba
        v = []
        for lnd in data:
            lnv=[]
            for i in range(len(lnd)):
                if grabable[i]=='n': continue
                lnv.append(lnd[i])
            v.append(lnv)

        return v

    #
    #
    #
    def GetPosition(self):
        return self.__grid.GetPosition()

    #
    #
    #
    def GetNRow(self):
        return self.__grid.GetGridCursorRow()   # -1 (No le quitamos pq fila 0 es el titulo

    #
    #
    #
    def GetNCol(self):
        return self.__grid.GetGridCursorCol()   # -1 (No le quitamos por el titulo)

    #
    #
    #
    def GetColEdi(self):
        return self.__edi

    #
    #
    #
    def SetDialog(self,dialogo,columna,fila=-1):
        if fila==-1:    # Para todas las filas
            self.__dlcols[columna]=dialogo
        else:
            self.__dlcells[(fila,columna)] = dialogo

    #
    #
    #
    def SetFmt(self,fmt,columna,fila=-1):
        grid = self.__grid

        if fila==-1:    # Para toda la columna
            self.__fmts[columna]=fmt
            for k in self.__fmtcells.keys:
                if k[1]==columna:
                    del self.__fmtcells[k]
        else:
            self.__fmtcells[(fila,columna)]=fmt

    #
    #
    #
    def GetFmt(self,columna,fila=-1):
        fmt = self.__fmts[columna]
        k = (fila,columna)
        if k in self.__fmtcells.keys():
            fmt = self.__fmtcells[k]
        return fmt

    #
    #-- IMPORTANTE !!!
    # Aquí solo entra si la celda no está editada, es decir, sólo
    #  cuando no se ha pulsado una letra/numero para escribir
    #
    def onKeyDown(self,event):
        grid = self.__grid
        key = event.GetKeyCode()
        col,fil = grid.GridCursorCol, grid.GetGridCursorRow()
        #
        if event.ControlDown():
            pass    # Se ha pulsado CTRL
            #if key==66: # B
            #    dl = self.__dlcols[col]
            #    dlc = self.__dlcells.get((fil,col),'')
            #    if dlc<>'': dl = dlc
            #    if dl<>'':  self.onPressButton(None)

        elif key in (wx.WXK_TAB, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, 316):
            self.Next_Cell()

        elif key in (wx.WXK_ESCAPE,314):
            self.Prev_Cell()

        else:
            event.Skip()


####################################
########  CELL EDITOR  ##############
####################################
class OC_CellEditor(wx_grid.PyGridCellEditor):
    def __init__(self,grid,pb,padre,fmt='l',lmax=0,dlsel='',edit='',fcal='',sobre='',ade='',cpan=''):
        self._grid = grid
        self._pb = pb
        self._padre = padre
        self._fmt = fmt
        self._lmax= lmax
        self._dlsel = dlsel
        self._edit = edit
        self._fcal = fcal
        self._sobre = sobre
        self._ade = ade
        self._cpan = cpan
        #-
        wx_grid.GridCellEditor.__init__(self)

    def Create(self, parent, id, evtHandler):
        pb = self._pb
        padre = self._padre
        fmt = self._fmt
        lmax= self._lmax
        dlsel = self._dlsel
        edit = self._edit
        fcal = self._fcal
        sobre = self._sobre
        ade = self._ade
        cpan =self._cpan

        #
        x,y = 0,0
        padre = parent
        if sys.platform=='win32':
            while padre<>self._pb:
                pos_padre = padre.GetPosition()
                x+=pos_padre[0]
                y+=pos_padre[1]
                padre= padre.Parent
            self._px, self._py = x,y
            self._padre = padre
        #
        entry = Entry.Entry(pb,padre,'GRIDENTRY',posic=(x,y),fmt=fmt,lmax=lmax,dlsel=dlsel)
        entry._grid = self._grid
        if edit in ('n','i'): entry.SetEditable(False)
        entry._ade = ade
        entry._fcal = fcal
        entry._sobre = sobre
        entry._cpan = cpan
        entry._grid = self._grid

        self._tc = entry
        self._tc.GetTextCtrl().SetInsertionPoint(0)
        self.SetControl(self._tc.GetTextCtrl())

        if evtHandler:
            self._tc.GetTextCtrl().PushEventHandler(evtHandler)

        self._tc.GetTextCtrl().Bind(wx.EVT_CHAR, self.OnChar)



    def SetSize(self,rect):
        tc = self._tc.GetTextCtrl()
        if sys.platform=='win32':
            pos_grid = self._grid.GetPosition()
            wtitu = self._grid.GetTituxSize()  # Alto de la fila de titulos

            x = self._px + rect.x + pos_grid.x
            y = self._py + rect.y + pos_grid.y + wtitu

            ancho = rect.width+2
            alto = rect.height+2
            tc.SetSize(x,y,ancho,alto,wx.SIZE_ALLOW_MINUS_ONE)
        else:
            tc.SetSize(rect.x, rect.y, rect.width+2, rect.height+2,wx.SIZE_ALLOW_MINUS_ONE)


    def BeginEdit(self,row,col,grid):
        # Formato de la Celda
        fmt = self._grid.GetFmt(col,row)
        ced = grid.GetCellEditor(row,col)
        ced._fmt = fmt
        self._tc.SetFmt(fmt)

        # Ponemos el valor
        value = grid.GetTable().GetValue(row,col)
        value = Funciones.Str_a_Fmt(value,fmt)
        self.startValue = value
        self._tc.SetValue(value,'n')
        self._tc.GetTextCtrl().SetInsertionPointEnd()
        self._tc.GetTextCtrl().SetSelection(0, self._tc.GetTextCtrl().GetLastPosition())
        self._tc.SetFocus()

    def ApplyEdit(self,row,col,grid):
        # This needs work/investigation as it's new in this version
        pass

    def EndEdit(self,row,col,grid,oldValue):
        changed = False
        self._tc.Formatea_Valor()
        val = self._tc.GetTextCtrl().GetValue()

        ade = self._ade
        if ade<>'':
            if (ade[:7]=='a_SELE:'):
                posibles = ade[7:].split('+')
                if not val in posibles:
                    return False

        if val != self.startValue:
            changed = True
            grid.GetTable().SetValue(row,col,val)

        self.startValue =''
        self._tc.GetTextCtrl().SetValue('')
        self._grid.Next_Cell()

        if changed: self._pb.Modifica=1

        return changed

    def Reset(self):
        self._tc.GetTextCtrl().SetValue(self.startValue)
        self._tc.GetTextCtrl().SetInsertionPointEnd()

    def Clone(self):
        return OC_CellEditor()

    def StartingKey(self,evt):
        #self._tc.GetTextCtrl().SetInsertionPointEnd() -> Hace que añada al final
        self.OnChar(evt)
        if evt.GetSkipped():
            self._tc.GetTextCtrl().EmulateKeyPress(evt)


    def StartingClick(self):
        pass

    def OnChar(self,evt):
        import string

        key = evt.GetKeyCode()
        try:
            char = chr(key)
        except:
            char = None

        if char<>None and char in string.printable:
            tipo = self._fmt
            valor = self._tc.GetTextCtrl().GetValue()
            if not (isinstance(valor,unicode) or isinstance(valor,str)):
                valor = str(valor)
            ok = Funciones.IsValid(key,tipo,valor)
            if ok: self._tc.GetTextCtrl().WriteText(char)
        else:
            evt.Skip()


#############################################
#
#
#############################################
if __name__ == "__main__":
    import Ventana

    app = wx.App(False)


    p1 = ['PANEL','P1',0,0,-1,-1,'','','',[]]

    #- ENTRADAS ANTES
    antes=[]
    antes.append(['E1','Código',10,15,6,'%',7,'','','','','ar_ls','codigo del cliente','clientes',''])
    antes.append(['E2','Nombre',-1,15,16,'l',10,'','','','','','','',''])
    p1[-1].append(['ENTRYS','EX',22,50,'','',antes])

    #- GRID
    cols=[]
    cols.append(['Artículo',6,'%',6,'','','','','','','','','',''])
    cols.append(['Nombre',30,'l',20,'n','n','','','','','','','',''])
    cols.append(['Fecha',7,'d',10,'','','','','','','','','',''])
    g1=['GRID','G1','Titulo',10,80,640,22,6,cols,0,'','']
    #
    p1[-1].append(g1)
    #

    #- ENTRADAS DESPUES
    desp=[]
    desp.append(['E3','Número',10,290,6,'2',7,'','','','','ar_ls','codigo del cliente','clientes',''])
    desp.append(['E4','Texto',-1,290,6,'l',10,'','','','','','','',''])
    desp.append(['E5','Fecha',-1,290,10,'d',10,'','','','','','','',''])
    p1[-1].append(['ENTRYS','EX',22,50,'F-25:25:0','B-0:0:0/F-255:255:255',desp])


    campos=[]
    campos.append(p1)
    #
    frame = Ventana.Ventana(None, 'Prueba Grid')
    frame.init_ctrls(campos)

    xxx=[]
    xxx.append(['0100',3100])
    xxx.append(['200',3120])
    frame._ct['G1'].SetValue(xxx)

    Funciones.debug(frame._ct['G1'].GetValue(),frame._ct['G1'].GetData())

    app.MainLoop()
