# -*- coding: utf8 -*-

import bsddb
import pickle
import datetime
import sys, os
import wx

try:
    from global_var import DIR_DATA
    from global_var import DIR_APL
except:
    DIR_IMG = '../../img'
    DIR_DATA = "."


#
#-- Funcion para mostrar mensajes de depuracion
#
def debug(*arg):
    txt = str(arg)
    dlg = wx.MessageDialog(None,txt,u'Debug',wx.OK)
    wx.Bell()
    dlg.ShowModal()
    dlg.Destroy()

#
#
#
def Men(texto,tipo='ok',img='x',titu='Mensaje'):
    #- Botones
    opt = wx.OK
    if tipo=='sn' or tipo =='Sn': opt = wx.YES_NO
    elif tipo=='sN': opt = wx.YES_NO | wx.NO_DEFAULT
    elif tipo=='oc': opt = wx.OK | wx.CANCEL
    #- Imagen
    img = wx.ICON_EXCLAMATION
    if img=='i': img = wx.ICON_INFORMATION
    elif img=='q': img = wx.ICON_QUESTION
    elif img=='e': img = wx.ICON_ERROR
    elif img=='w': img =wx.ICON_WARNING

    opt =opt | img
    dlg = wx.MessageDialog(None,texto,titu,opt)
    retCode = dlg.ShowModal()
    #- Respuesta
    respu = None
    if retCode == wx.ID_YES: respu = 's'
    elif retCode== wx.ID_NO: respu = 'n'
    elif retCode == wx.ID_CANCEL: respu = 'c'
    elif retCode == wx.ID_OK: respu = 'o'
    #
    dlg.Destroy()
    return respu

#
#-- Crea un dialogo para petición de datos
#
def Entra_dlg(padre=None,titu='',text='Introduce Dato',value=''):
    dlg = wx.TextEntryDialog(padre,text,titu,value, style =wx.OK|wx.CANCEL)
    respu = None
    if dlg.ShowModal()==wx.ID_OK:
        respu = dlg.GetValue()
    dlg.Destroy()
    return respu
#
#
#
def List_dlg(padre=None,titu='',text='Seleccione',choices=[],size=(200,200)):

    dlg = wx.SingleChoiceDialog(padre,text,titu,choices)
    respu = None
    if dlg.ShowModal()==wx.ID_OK:
        respu = dlg.GetSelection()
    dlg.Destroy()
    return respu

#
#
#
def Progress_dlg(titu='',text='Esperando...',max=100):

    dlg = wx.ProgressDialog(titu,text,max)
    dlg.Update(0)   # Actualiza el valor de progreso
                    # Cerrar con dlg.Destroy()
    return dlg

#
#
#
def File_dlg(padre=None,titu='Elegir Fichero',tipos=['*']):
    import os

    wildcard=''
    for tipo in tipos:
        if wildcard<>'': wildcard+='|'
        wildcard += '(*.'+tipo+')|*.'+tipo
    #
    dlg = wx.FileDialog(padre,titu,os.getcwd(),'',wildcard,wx.OK)
    respu = None
    if dlg.ShowModal()==wx.ID_OK:
        respu = dlg.GetPath()
    dlg.Destroy()

    return respu



#
#-- Ajusta con ceros a la izquierda a la longitud maxima
#
def ajus0(cad,max):
    cad = str(cad)
    return cad.zfill(max)

#
#-- Devuelve una copia del objeto pasado como argumento
#
def copia_rg(obj):
    copia = pickle.loads(pickle.dumps(obj))
    return copia


#
#-- Devuelve una fecha en formato entero.
#
def Fecha(fmt=''):
    """ Devuelve la Fecha Actual en el formato indicado
        fmt =''     --> Formato Número (Defecto)
        fmt ='str'  --> Formato Cadena dd/mm/aaaa
        fmt = 'y'   --> Año Actual en Número
        fmt = 'm'   --> Mes Actual en Numero (1 a 12)
        fmt = 'd'   --> Día Actual en Numero
        fmt = 'hm'  --> Hora Actual
    """
    fini = datetime.date(2000,1,1)    # Fecha inicial = 01 - Enero - 2000
    hoy = datetime.datetime.now()
    resul = None
    #
    if fmt=='': # Fecha Actual
        hoy = hoy.date()
        dif = hoy - fini
        resul = dif.days
    elif fmt=='str':   # Fecha actual en cadena
        resul = hoy.strftime('%d/%m/%Y')
    elif fmt=='y':      # Año en Numero
        resul = hoy.year
    elif fmt=='m':      # Mes actual (1 a 12)
        resul = hoy.month
    elif fmt=='d':      # Dia en numero
        resul = hoy.day
    elif fmt=='hm':
        h = hoy.hour
        m = hoy.minute
        resul = str(h).zfill(2)+':'+str(m).zfill(2)
    #
    return resul
#
#-- Pasa una fecha con formato numero a una fecha con formato texto
#
def Num_aFecha(fecha,fmt=''):
    """ Combierte una fecha en formato número a formato Texto (fmt='')
    o devuelve como enteros dia, mes o año de la fecha indicada
    (fmt='d','m' o 'y')"""

    if fecha==None or fecha=='':
        return ''

    fini = datetime.date(2000,1,1)
    try:
        fecha = fini + datetime.timedelta(days=fecha)
    except:
        debug(fecha,'No es una fecha valida.')


    if fmt=='': # Fecha Actual
        resul = fecha.strftime('%d/%m/%Y')
    elif fmt=='y':      # Año en Numero
        resul = fecha.year
    elif fmt=='m':      # Mes actual (1 a 12)
        resul = fecha.month
    elif fmt=='d':      # Dia en numero
        resul = fecha.day

    return resul

#
#-- Pasa una fecha con formato texto a una fecha con formato numero
#
def Fecha_aNum(strfecha):
    """ Combierte una fecha con formato texto a formato número """
    fini = datetime.date(2000,1,1)    # Fecha inicial = 01 - Enero - 2000
    sep='/'
    if strfecha.find('-')>0: sep='-'
    fec = strfecha.split(sep)
    if len(fec)<>3: return None
    try:
        fec = datetime.date(int(fec[2]),int(fec[1]),int(fec[0]))
        dif = fec - fini
        fec = dif.days
    except:
        fec = None

    return fec
#
#-- Sumar a Fecha Dias o Semanas
#
def Sm_Fecha(fecha,num,fmt='d'): # fmt: d = dias ; w = semanas
    """ Devuelve una fecha resultado de sumar 'num' dias o semanas.
        fmt = 'd' --> Sumar Dias
        fmt = 'w' --> Sumar Semanas
    """
    fini = datetime.date(2000,1,1)
    fecha = fini + datetime.timedelta(days=fecha)
    fsuma = None
    if fmt=='d':
        fsuma = fecha + datetime.timedelta(days=num)
    elif fmt=='w':
        fsuma = fecha + datetime.timedelta(weeks=num)
    else:
        return None

    dif = fsuma - fini
    fec = dif.days

    return fec

#
#-- Devuelve los dias de diferencia entre dos fechas
#
def Df_Fechas(fmin,fmax):
    """ Devuelve los dias de diferencia entre dos fechas """
    fini = datetime.date(2000,1,1)
    fmin = fini + datetime.timedelta(days=fmin)
    fmax = fini + datetime.timedelta(days=fmax)
    dif = fmax - fmin

    return dif.days

#
#-- Comprueba que la tecla sea válida para el formato indicado
#
def IsValid(key,fmt,cadena=''):
    """ Comprueba que la tecla pulsada sea válida para el formato
    indicado, llevando ya escrita la cadena 'cadena' """

    valido = True

    if fmt in ('i','d','0','1','2','3','4','5','6','7','8','9'):
        # Comprobamos que lo introducido son numeros
        if key<48: valido=False         # 48 a 57 = 1 a 0 teclas arriba
        elif key>57 and key<324: valido=False
        elif key>333: valido=False      # 324 a 333 = 1 a 0 teclas numpad

        # Para números permitimos (-), pero solo en la primera posicion
        if fmt in ('i','0','1','2','3','4','5','6','7','8','9'):
            if key==45 and cadena=='':
                valido=True

        # Para numeros decimales permitimos el punto, siempre y cuando
        # no se hayan excedido el num maximo de decimales indicados
        if fmt not in ('i','d','0'):
            pospunto = cadena.find('.')
            if pospunto>=0:
                if key==46: #wx.WXK_DECIMAL or key==wx.WXK_NUMPAD_DECIMAL:
                    valido=False    # Ya había un punto
                else:
                    if len(cadena)-pospunto > int(fmt):
                        valido=False
            elif key==46: #wx.WXK_DECIMAL or key==wx.WXK_NUMPAD_DECIMAL:
                valido = True

    return valido

#
#-- Devuelve el valor de la cadena 'cadena' en el formato 'fmt'
#
def Str_a_Fmt(cadena,fmt):
    """ Devuelve el valor de la cadena 'cadena' en el formato 'fmt' """
    resul = cadena
    #
    if fmt=='d':
        resul = Fecha_aNum(cadena)
    elif fmt=='i':
        try:
            resul = int(resul)
        except:
            resul=0
    elif fmt in ('0','1','2','3','4','5','6','7','8','9'):
        try:
            resul = float(fmt)
        except:
            resul=0.0
    #
    return resul

#
#-- Convierte el valor 'valor' (en formato 'fmt') a una cadena de texto
#
def Fmt_a_Str(valor,fmt):
    """ Convierte el valor 'valor' (en formato 'fmt') a una cadena de texto """
    if not isinstance(valor, unicode):
        resul = str(valor)
    else:
        resul = valor

    if fmt=='d':
        resul = Num_aFecha(valor)
    elif fmt in ('i','0'):
        valor = str(valor)
    elif fmt in ('1','2','3','4','5','6','7','8','9'):
        valor = str(valor)
        if valor.find('.')==-1: valor = valor+'.'
        ent,dec = valor.split('.')
        while len(dec)<int(fmt):
            dec = dec + '0'
        valor = ent+'.'+dec
    else:
        if not isinstance(resul, unicode):
            resul = resul.decode('latin-1')

    return resul


#
#-- Envia el Foco a un objeto (
#
def Foco(pb,nombre):
        if nombre<>None:
            try:
                obj = pb._ct[nombre]
                obj.SetFocus()
            except:
                Men(Busca_Error())
        else:
            pass
            #pb._ct[pb._ct.keys[0]].SetFocus()

#
#-- Devuelve un mensaje detallado con el error ocurrido en una excepci�n
#
def Busca_Error(maxTBlevel=5):
    import sys
    import traceback
    #
    cla,exc,trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__['args']
    except:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)

    return '\n'.join([str(excName),str(excArgs),str(excTb)])

#
#
#
def claves(file):
    if isinstance(file,str):
        ruta_datos = DIR_DATA +'/'+ file + '.db'
        bt = bsddb.btopen(ruta_datos)
        res = bt.keys()
        bt.close()
    else:
        res = file.keys()
        
    return res

#
#-- Devuelve los datos de un fichero/diccionario
#
def lee_dicc(fichero,key,ruta=None):
    if ruta == None: ruta = DIR_APL
    ruta_fichero = ruta+'/'+fichero

    try:
        f = bsddb.btopen(ruta_fichero)
        datos = pickle.loads(f[key])
        f.close()
    except:
        Men('No se pudo leer '+key+' de '+ruta_fichero+'\n'+Busca_Error())
        datos={}

    return datos

#
#-- Graba los datos dados en un fichero/diccionario
#
def graba_dicc(fichero,key,datos,ruta=None):
    if ruta == None: ruta = DIR_APL
    ruta_fichero = ruta+'/'+fichero

    try:
        f = bsddb.btopen(ruta_fichero)
        f[key] = pickle.dumps(datos)
        f.close()
    except:
        Men('No se pudo grabar '+key+' de '+fichero+'\n'+Busca_Error())
        return None

    return 0
#
#
#
def borra_dicc(fichero,key,ruta=None):
    if ruta == None: ruta = DIR_APL
    ruta_fichero = ruta+'/'+fichero

    try:
        f = bsddb.btopen(ruta_fichero)
        del f[key]
        f.close()
    except:
        Men('No se pudo borrar '+key+' de '+fichero+'\n'+Busca_Error())
        return None

    return 0

#
#-- Claves de un fichero/diccionario con ruta
#
def claves_dicc(fichero,key,ruta=None):
    if ruta == None: ruta = DIR_APL
    
    if isinstance(file,str):
        ruta_fichero = ruta+'/'+fichero
        try:
            f = bsddb.btopen(ruta_fichero)
            k = f.keys()
            f.close()
        except:
            k = None
    else:
        try:
            k = fichero.keys()
        except:
            k = None

    return k

#
#-- Lee un registro de la Base de datos
#
def lee(file,key):

    if isinstance(file,str):
        ruta_datos = DIR_DATA +'/'+ file + '.db'
        #- No estamos actualizando, leer del fichero
        f = bsddb.btopen(ruta_datos)
        try:
            rg = pickle.loads(f[key])
        except:
            rg=1

        f.close()
    else:
        rg = pickle.loads(file[key])    # Se pas� el puntero al fichero

    # Falta darle el formato correcto a los campos !!!

    return rg

#
#- Hace una selecci�n de datos
#
def select(fichero,campos,preguntas=[],orden=[]):

    if isinstance(campos,str): campos = campos.split(' ')
    
    ruta_datos = DIR_DATA +'/'+ fichero + '.db'
    fichero = bsddb.btopen(ruta_datos)

    keys = claves(fichero)
    resul=[]
    for key in keys:
        rg = lee(fichero,key)
        cumple = 1
        for preg in preguntas:
            campo,op,valor = preg
            if campo=='0':
                rg_valor=key
            else:
                if not campo in rg.keys(): continue # Pregunta inventada
                rg_valor = rg[campo]

            if isinstance(rg_valor,str):
                rg_valor = rg_valor.upper()
                valor = str(valor).upper()
                if op=='=': cumple = (valor in rg_valor)
                elif op=='<>': cumple = not(valor in rg_valor)
                else: cumple = eval('"'+rg_valor+'"' + op + '"'+valor+'"')
            else:
                if op=='=': op='=='
                cumple = eval(str(rg_valor)+op+str(valor))
            if not cumple: break

        if cumple:
            aux=[]
            for ctrl in campos:
                if ctrl=='0':  
                    aux.append(key)
                else: 
                    if ctrl in rg.keys(): aux.append(rg[ctrl])
                    else: aux.append('')
            if len(aux)==1: aux = aux[0]
            resul.append(aux)
    resul.sort()
    return resul

#
#- Hace una actualizaci�n de un registro
#
def p_actu(file,idx,rg):
    #
    if file=='':
        Men('No ha definido tabla sobre la que grabar.')
        return (-1,'')
    if idx=='':
        Men('No se ha definido correctamente el campo codigo de registro')
        return (-1,'')

    ##if not file in globals()['P_ACTU']: globals()['P_ACTU'][file]={}
    ##globals()['P_ACTU'][file][idx]=rg

    if isinstance(file,str):
        ruta_datos = DIR_DATA +'/'+ file + '.db'
        f = bsddb.btopen(ruta_datos)
        f[idx] = pickle.dumps(rg)
        f.close()
    else:
        file[idx] = pickle.dumps(rg)    # file era el puntero al fichero
    
#
#
#
def rg_vacio(archivo):
    dicc = bsddb.btopen(DIR_APL+'/dicc')
    if not archivo in dicc:
        Men('rg_vacio: No se ha definido la tabla '+filedb+'.')
        return None
    campos = pickle.loads(dicc[archivo])[-1] # Ultima posicion tiene la lista de campos
    dicc.close()
    reg={}
    for ln in campos:
        key,deno,fmt = ln[:3]
        if fmt in ('l','%'): reg[key]=''
        elif fmt in ('i','0','1','2','3','4','5','6','7','8','9'): reg[key]=0
        elif fmt in ('d'): reg[key]=None
        else: reg[key]=[]
    return reg

#
#-- Devuelve el primer codigo libre de un fichero
#
def u_libre(archivo):
    ruta_datos = DIR_DATA +'/'+ archivo + '.db'
    f = bsddb.btopen(ruta_datos)
    ls = f.keys()
    f.close()
    
    ls.sort()
    if ls==[]:
        next = '0'
    else:
        cod = ls[-1]
        next = Busca_Prox(cod)
    
    return next
    
#
#
#
def Busca_Prox(valor):
    try:
        i = int(valor)
        i+=1
        cod = ajus0(i,len(valor))
        if len(cod)>len(valor): a=1/0   # Lanzar expecion
    except:
        li=[]
        for c in valor: li.append(ord(c))
        
        ult = li[-1]
        if ult == ord('9'): 
            li[-1] = ord('A')
        else:
            li[-1] = li[-1] + 1 
            
        lc=[]
        for i in li: lc.append(chr(i))
        
        cod = ''.join(lc)
    
    return cod
    

#
#
#
def Crea_Info(padre,fichero,informe,destino=''):
    import  wx.lib.printout as  printout
    import dl_select

    ls_inf = lee_dicc('forms',fichero, os.path.join(DIR_APL,'manage'))
    if not informe in ls_inf.keys(): return -1
    #
    deno,acc_antes,accion,acc_despues,gridc,gridp = ls_inf[informe]
    #
    if isinstance(deno, unicode):
        deno = deno.decode('latin-1').encode('utf8')

    #- Contruimos preguntas
    preguntas = []
    for ln in gridp:
        campo, titu ,fmt, lmax, op = ln
        preguntas.append([titu,op,'',campo,fmt,lmax])

    #- Campos a mostrar
    campos=[]
    titus=[]
    formatos=[]
    anchos=[]
    for ln in gridc:
        campos.append(ln[0])
        titus.append(ln[1].decode('latin-1').encode('utf8'))
        formatos.append(ln[2])
        anchos.append(ln[3]/12.0)
    #-
    #if acc_antes<>'':
    #    pb.Ejecuta_Accion(acc_antes)

    if accion<>'':
        campos = '0'
        dl = dl_select.dl_select(padre,fichero,campos,preguntas)
        res,prg = dl.res()
        if res==None: return -1
        res = padre.Ejecuta_Accion(accion,args=[res,prg])
    else:
        dl = dl_select.dl_select(padre,fichero,campos,preguntas)
        res,prg = dl.res()
        if res==None: return -1


    #if acc_despues<>'':
    #        pb.Ejecuta_Accion(acc_despues)

    if destino=='':
        for ln in res:
            for i in range(len(ln)):
                if formatos[i]=='d': ln[i] = Num_aFecha(ln[i])
                if formatos[i] in ['i','0','1','2','3','4']: ln[i] = str(ln[i])
                #
                #if not isinstance(ln[i],str):
                ln[i] = ln[i].decode('latin-1').encode('utf8')

        prt = printout.PrintTable(padre)
        prt.data = res
        prt.set_column = anchos #[ 1, 3, 1, 1, 2]
        prt.label = titus
        for i in range(len(formatos)):
            fmt = formatos[i]
            if fmt in ['i','0','1','2','3','4','5','6','7','8','9']:
                prt.SetColAlignment(i,wx.ALIGN_RIGHT)

        #prt.SetColAlignment(1, wx.ALIGN_CENTRE)
        #prt.SetColBackgroundColour(0, wx.NamedColour('RED'))
        #prt.SetColTextColour(0, wx.NamedColour('WHITE'))
        #prt.SetCellColour(4, 0, wx.NamedColour('LIGHT BLUE'))
        #prt.SetCellColour(4, 1, wx.NamedColour('LIGHT BLUE'))
        #prt.SetCellColour(17, 1, wx.NamedColour('LIGHT BLUE'))
        #
        #prt.SetColBackgroundColour(2, wx.NamedColour('LIGHT BLUE'))
        #prt.SetCellText(4, 2, wx.NamedColour('RED'))

        #prt.SetColTextColour(3, wx.NamedColour('RED'))
        prt.label_font_colour = wx.Colour('WHITE')
        prt.SetHeader(deno, colour = wx.Colour('RED'))

        prt.SetHeader("Impreso: ", type = "Date & Time", align=wx.ALIGN_RIGHT, indent = -1, colour = wx.Colour('BLUE'))
        prt.SetFooter("Page No", colour = wx.Colour('RED'), type ="Num")
        prt.Preview()

    else:
        padre._ct[destino].SetValue(res)
