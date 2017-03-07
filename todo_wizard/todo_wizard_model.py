# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions

import logging
_logger = logging.getLogger(__name__)
_logger.debug('desbichando')
_logger.info('Informacion')
_logger.warning('Te lo advierto')
_logger.error('Muy mal')

class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    task_ids = fields.Many2many('todo.task', string='Tareas')
    new_deadline = fields.Date('FechaLimite a poner')
    new_user_id = fields.Many2one('res.users',string='Poner responsable')

    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        if not (self.new_deadline or self.new_user_id):
            raise exceptions.ValidationError('nada que actualizar')
        _logger.debug('Actualizacion masiva de tareas %s',self.task_ids.ids)
        if self.new_deadline:
            self.task_ids.write({'date_deadline':self.new_deadline})
        if self.new_user_id:
            self.task_ids.write({'user_id':self.new_user_id.id})
        return True

    @api.multi
    def do_count_task(self):
        Task = self.env['todo.task']
        count = Task.search_count([('is_done','=',False)])
        raise exceptions.Warning('Hay %d tareas activas' % count)

    @api.multi
    def do_reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }

    @api.multi
    def do_populate_task(self):
        self.ensure_one()
        Task = self.env['todo.task']
        all_tasks = Task.search([])
        self.task_ids = all_tasks
        return self.do_reopen_form()
