from odoo import models, fields

class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Giảng viên'
    _order = 'name'

    user_id = fields.Many2one(
        'res.users',
        string='Tài khoản người dùng',
        required=True,
        ondelete='cascade'
    )

    code = fields.Char(string='Mã giảng viên', required=True)
    name = fields.Char(string='Họ tên', required=True)
    degree = fields.Char(string='Trình độ', help='VD ThS, TS, PGS, GS')
    major = fields.Char(string='Chuyên ngành')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Số điện thoại')

    department_id = fields.Many2one(
        'school.department',
        string='Khoa công tác',
        required=True)

    department_head_ids = fields.One2many(
        'school.department',
        'head_id',
        string='Khoa làm trưởng')

    advised_class_ids = fields.One2many(
        'school.class',
        'advisor_id',
        string='Lớp cố vấn')