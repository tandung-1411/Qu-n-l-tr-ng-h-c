from odoo import models, fields

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'Môn học'
    _order = 'name'
    code = fields.Char(string='Mã môn học', required=True)
    name = fields.Char(string='Tên môn học', required=True)
    credits = fields.Integer(string='Số tín chỉ', required=True)
    prerequisite_id = fields.Many2one(
        'school.subject',
        string='Môn tiên quyết')
    department_id = fields.Many2one(
        'school.department',
        string='Khoa phụ trách',
        required=True)