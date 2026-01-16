from odoo import models, fields

class AcademicYear(models.Model):
    _name = 'school.academic.year'
    _description = 'Năm học'
    _order = 'name desc'

    name = fields.Char(string='Năm học', required=True, help='VD: 2025-2026')
    start_date = fields.Date(string='Ngày bắt đầu')
    end_date = fields.Date(string='Ngày kết thúc')
    semester_ids = fields.One2many('school.semester', 'year_id', string='Các học kỳ')