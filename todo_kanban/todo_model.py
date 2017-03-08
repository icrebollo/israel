# -*- coding: utf-8 -*-
from openerp import models, fields
class TodoTask(models.Model):
    _inherit = 'todo.task'
    priority = fields.Selection([('0','Baja'),('1','Normal'),('2','Alta')])
    kanban_state = fields.Selection([('normal','En progreso'),('blocked','Bloqueado'),('done','Listo para seguir')],
                                    'kanban_state',default='Normal')