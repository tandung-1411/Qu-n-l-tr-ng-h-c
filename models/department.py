from odoo import models, fields

class Department(models.Model):
    _name = 'school.department'
    _description = 'Khoa'
    _order = 'name'
    code = fields.Char(string='Mã khoa', required=True)
    name = fields.Char(string='Tên khoa', required=True)
    establishment_date = fields.Date(string='Ngày thành lập')
    head_id = fields.Many2one(
        'school.teacher',
        string='Trưởng khoa')