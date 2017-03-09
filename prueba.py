# -*- coding: utf-8 -*-
from openerp import models

class mi_clase(models.Model):
    _inherit = 'usuarios.estudiantes'

#    var = self.browse(cr, uid, 4)

    # Fin de mi_clase

#    print 'Nombre del estudiante: ', var.name

 #   for item in var.materias_ids:
 #       print 'Materia: ', item.name
 #       print 'Profesor: ', item.profesor
 #       print 'Nota: %2.2f' % item.nota