import erppeek
from bs4 import BeautifulSoup


class ContarTraduccionesPeek():
    def __init__(self):
        self.api = erppeek.Client('http://localhost:8069', 'v8dev', 'admin', 'admin')
        self.model = self.api.model('ir.translation')
        recs = self.model.search([('lang','=','es_ES')])
        self.datos = self.model.read(recs, ['name', 'lang','value','type'])

    def leertabla(self):

        print self.model.count([('lang', '=', 'es_ES')])

        frase_larga = 0
        num_frase_larga = 0
        hueco = 0
        for r in self.datos:
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

            hueco += 1
            # from pprint import pprint
            # pprint(traduccion)
            # pprint(r['type'])
        print hueco, num_frase_larga
        return True


if __name__ == '__main__':
    apipeek = ContarTraduccionesPeek()
    res = apipeek.leertabla()
