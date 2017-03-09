# -*- coding: utf-8 -*-
from openerp import models, fields
class TodoTask(models.Model):
    _inherit = 'todo.task'
    priority = fields.Selection([('0','Baja'),('1','Normal'),('2','Alta')],'Priority', default='0')
    kanban_state = fields.Selection([('normal','En progreso'),
                                     ('blocked','Bloqueado'),
                                     ('done','Listo para seguir')],
                                    'kanban state',default='normal')

    color = fields.Integer('Color Index')

    company_id = fields.Many2one(
        related='user_id.company_id',
        string='Company',
        store=True)

