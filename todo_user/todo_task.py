# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['todo.task','mail.thread']
    name = fields.Char(help="¿Que necesitas?")
    user_id = fields.Many2one('res.users', 'Responsible')
    date_deadline = fields.Date('Deadline')

    @api.multi
    def do_clear_done(self):
        domain = [('is_done', '=', True),'|',('user_id', '=', 'self.env.uid')]
        done_recs = self.search(domain)
        done_recs.write({'active':False})
        return True

    @api.one
    def do_toggle_done(self):
        if self.user_id != self.env.user:
            raise exceptions.Warning('Solo lo hace el responsable')
        else:
            return super(TodoTask,self).do_toggle_done()

    @api.model
    def create(self, vals):
        # cosas antes
        new_record = super(TodoTask,self).create(vals)
        # cosas despues
        return new_record

    @api.multi
    def write(self, vals):
        # cosas antes
        super(TodoTask,self).write(vals)
        # cosas despues
        return True
