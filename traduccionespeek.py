import erppeek


class ContarTraduccionesPeek():

    def __init__(self,srv,db,user,pwd):
        api = erppeek.Client('http://localhost:8069', 'v8dev', 'admin', 'admin')

        api.common.version()
        api.count('res.partner', [])
        api.search('ir.translate',)