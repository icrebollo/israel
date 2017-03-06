# -*- coding: utf-8 -*-
from openerp import models, fields, api
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
            raise Exception('Solo lo hace el responsable')
        else:
            return super(todo.task,self).do.toggle_done()

