# -*- coding: utf-8 -*-
import xmlrpclib
from bs4 import BeautifulSoup

class ContarTraducciones():
    def __init__(self,srv,db,user,pwd):
        common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' %srv)
        self.api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' %srv)
        self.uid = common.authenticate(db, user, pwd, {})
        self.pwd = pwd
        self.db = db
        self.model = 'ir.translation'

    def execute(self, method, arg_list, kwarg_dict=None):
        res = self.api.execute_kw(self.db, self.uid, self.pwd, self.model, method, arg_list, kwarg_dict or {})
        return res

    def leertabla(self):
        domain = [('lang','=','es_ES')] #,('value','like','vinculadas con')] ('type','=','selection')
        fields = ['name', 'lang','value','type']
        return self.execute('search_read',[domain, fields])

if __name__ == '__main__':
    srv, db = 'http://localhost:8069', 'v8dev'
    user, pwd = 'admin', 'admin'
    api = ContarTraducciones(srv, db, user, pwd)
    res = api.leertabla()
    #from pprint import pprint
    numero_traduc = 0
    palabara_larga = 0
    frase_larga = 0
    num_frase_larga = 0
    hueco = 0
    for r in res:
        frase_larga = 0
        traduccion = r['value']
        soup = BeautifulSoup(traduccion)
        for tag in soup.find_all(True):
            if tag.string is not None:
                traduccion = tag.string

        palabra = ""
        for s in traduccion:
            if s == ' ':
                frase_larga += 1
                if palabra != '':
                    hueco = hueco + 1
                    if len(palabra) > 2:
                        palabara_larga += 1
                    if len(palabra) == 1:
                        if palabra not in 'aeiouy':
                            hueco -= 1
                    if len(palabra) == 2:
                        if palabra[0] == '%' or palabra[1] == '%':
                            hueco -= 1
                        elif palabra[0] in '0123456789' or palabra[1] in '0123456789':
                            hueco -= 1
                    palabra = ""
            else:
                palabra = palabra + s
        if frase_larga > 5:
            num_frase_larga += 1

        palabara_larga += 1
        hueco += 1
        #pprint(traduccion)
        #pprint(r['type'])
        numero_traduc = numero_traduc + 1
    print numero_traduc, hueco, palabara_larga, num_frase_larga