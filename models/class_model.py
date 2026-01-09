from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Lớp'
    _order = 'name'
    code = fields.Char(string="Mã lớp",required=True)
    name = fields.Char(string="Tên lớp",required=True)
    course_code = fields.Char(string="Khóa học", help='Ví dụ: K20, K21')
    start_year = fields.Date(string='Thời gian bắt đầu')
    department_id = fields.Many2one(
        'school.department',
        string='Khoa quản lý',
        required=True,)
    advisor_id = fields.Many2one(
        'school.teacher',
        string='Cố vấn học tập')
    student_ids = fields.One2many(
        'school.student',
        'class_id',
        string='Danh sách sinh viên')