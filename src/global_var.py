import os,sys,wx

#DIR_BASE = os.path.join(os.path.expanduser("~"),"gesPelu")
#DIR_APL = os.path.join(DIR_BASE,"src")
#DIR_DATA = os.path.join(DIR_BASE,"data")
#DIR_IMG = os.path.join(DIR_BASE,"img")


#xxx = sys.argv[0]   # Ruta hacia el fichero que se ejecuta al inicio
#xxx = xxx.split('/')
#xxx = '/'.join(xxx[:-1])
xxx = path = os.path.dirname(__file__)
DIR_APL = xxx  # Ruta menos nombre del fichero que se ejecuta
DIR_BASE = DIR_APL[:-3]   # Ruta menos src/

if DIR_APL=='':
    #DIR_BASE = os.path.join(os.path.expanduser("~"),"gesPelu")
    #DIR_APL = os.path.join(DIR_BASE,"src")
    wx.MessageDialog(None,'No se pudo obtener directorio de inicio','ERROR')

DIR_DATA = os.path.join(DIR_BASE,"data")
DIR_IMG = os.path.join(DIR_BASE,"img")


print('DIR_APL',DIR_APL)
print('DIR_BAS',DIR_BASE)
print('DIR_IMG',DIR_IMG)

if not DIR_APL in sys.path: sys.path.insert(0,DIR_APL)

TAB ='\t'
NL  ='\n'

ACTU_PTES={}

