from odoo import models, fields

class Semester(models.Model):
    _name = 'school.semester'
    _description = 'Học kỳ'

    name = fields.Selection([
        ('hk1', 'HK1'),
        ('hk2', 'HK2'),
        ('hkhe', 'HK Hè')
    ], string='Học kỳ', required=True, default='hk1')

    year_id = fields.Many2one('school.academic.year', string='Năm học', required=True, ondelete='cascade')
    start_date = fields.Date(string='Ngày bắt đầu')
    end_date = fields.Date(string='Ngày kết thúc')