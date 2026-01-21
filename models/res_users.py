from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    student_ids = fields.One2many(
        'school.student',
        'user_id',
        string='Hồ sơ sinh viên'
    )