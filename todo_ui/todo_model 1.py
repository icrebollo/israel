# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons.base.res import res_request

def referencable_models(self):
    return res_request.referencable_models(
        self,self.env.cr, self.env.uid, context=self.env.context)


class Tag(models.Model):
    _name = 'todo.task.tag'
    _parent_store = True
    name = fields.Char('Nombre', size=40, translate=True)
    task_ids = fields.Many2many(string='Tasks')
    parent_id = fields.Many2one('todo.task.tag','Parent Tag',ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    child_ids = fields.One2many('todo.task.tag', 'parent_id', 'Child Tags')

class Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence,name'
    _rec_name = "name"  # por defecto
    _table = 'todo_task_stage'  # por defecto
    name = fields.Char('Name', size=40, translate=True)
    sequence = fields.Integer('Sequence')
    tasks = fields.One2many('todo.task','stage_id','Tareas enla etapa')
    fold = fields.Boolean('Fold')
    #state = fields.Selection(['Activo','apagado','libre'])

class TodoTask(models.Model):
    _inherit = 'todo.task'
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tags_id = fields.Many2many('todo.task.tag', string='Tags')
    #refers_to = fields.Reference([('res.user', 'User'), ('res.partner', 'Partner')], 'Refers to')
    refers_to = fields.Reference(referencable_models, 'Refers to')
    stage_fold = fields.Boolean(
        string='Stage_folded?',
        compute='_compute_stage_fold')
    search = '_search_stage_fold'
    inverse = '_write_stage_fold'

    #stage_state = fields.Many2one(related='stage_id.state',string="Estado escena")

    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold
