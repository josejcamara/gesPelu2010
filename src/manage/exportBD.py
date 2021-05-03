#!/usr/bin/env python
# -*- coding: utf8 -*-

""" Export forms and dicc data from berkeleyDB to SQLite """

import model_dicc_bsddb
import model_dicc
import os,sys

def confirm(message):
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = raw_input(message + " [Y/N]? ").lower()
    return answer == "y"

def exportForms():
    print('Exportando forms...')

    # lis=[]
    # forms = bsddb.btopen('forms')
    # for dc in forms.keys():
    #     datos = pickle.loads(forms[dc])
    #     # dc: Diccionario al que está asociado este informe/listado
    #     # datos: __dict__ , Key: formId , Value: [
    #     #                                   descripcion, 
    #     #                                   accAntes, 
    #     #                                   accRelleno, 
    #     #                                   accDespues, 
    #     #                                   columnas(campo,titulo,fmt,len,fcal)
    #     #                                 ] 
    #     print (dc, datos)
    #     break
    # forms.close()

def exportDicc():
    if os.path.exists('dicc.db'):
        print('BD destino ya existe. Borra antes de ejecutar este proceso.')
        return
    #
    print('Exportando dicc...')
    #
    diccBSD = model_dicc_bsddb.Dicc('.')
    diccSQL = model_dicc.Dicc('.')
    #
    diccList = diccBSD.getDiccList()
    for nombreTabla,descTabla in diccList:
        diccHeaderData = diccBSD.getDiccHeader(nombreTabla)
        diccRowsData = diccBSD.getDiccRows(nombreTabla)

        print(" ... Exportando %s " % nombreTabla)
        status = diccSQL.updateDicc(nombreTabla, diccHeaderData, diccRowsData)
        if status != 0:
            raise ValueError('No se pudo exportat %s' % nombreTabla)
    #
    print('Proceso finalizado.')


def main():
    doDicc = confirm('¿Quieres exportar los dicc?')
    if (doDicc):
        exportDicc()

    doForms = confirm('¿Quieres exportar los forms?')
    if (doForms):
        exportForms()


#############################################################
#
#
#
##############################################################
if __name__ == "__main__":
    main()