from odoo import models, fields, api

class Student(models.Model):
    _name = 'school.student'
    _description = 'Sinh viên'
    code = fields.Char(string='Mã sinh viên', required=True)
    name = fields.Char(string='Họ tên', required=True)
    birth_date = fields.Date(string='Ngày sinh', required=True)
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string='Giới tính', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Số điện thoại', required=True)
    status = fields.Selection([
        ('active', 'Đang học'),
        ('suspended', 'Tạm dừng'),
        ('graduated', 'Tốt nghiệp')
    ], string='Trạng thái', default='active')

    class_id = fields.Many2one(
        'school.class',
        string='Lớp')
    department_id = fields.Many2one(
        'school.department',
        string='Khoa',
        related='class_id.department_id',
        store=True,
        readonly=True)
    enrollment_ids = fields.One2many('school.enrollment', 'student_id', string='Đăng ký môn học')
    grade_ids = fields.One2many('school.grade', 'student_id', string='Điểm môn học')
    gpa_4 = fields.Float(string='GPA (hệ 4)', compute='_compute_gpa', store=True, digits=(3, 2))
    average_10 = fields.Float(string='Điểm TB (hệ 10)', compute='_compute_gpa', store=True, digits=(3, 2))

    academic_performance = fields.Selection([
        ('weak', 'Yếu'),
        ('average', 'Trung bình'),
        ('fair', 'Khá'),
        ('good', 'Giỏi'),
        ('excellent', 'Xuất sắc')
    ], string='Học lực', compute='_compute_gpa', store=True)

    @api.depends('grade_ids.total_score', 'grade_ids.result', 'grade_ids.enrollment_id.credits')
    def _compute_gpa(self):
        for student in self:
            passed_grades = student.grade_ids.filtered(lambda g: g.result == 'pass' and g.enrollment_id)
            if passed_grades:
                total_credits = sum(passed_grades.mapped('enrollment_id.credits'))
                if total_credits > 0:
                    weighted_sum_10 = sum(g.total_score * g.enrollment_id.credits for g in passed_grades)
                    avg_10 = weighted_sum_10 / total_credits
                    student.average_10 = round(avg_10, 2)

                    if avg_10 >= 8.5:
                        gpa4 = 4.0
                    elif avg_10 >= 8.0:
                        gpa4 = 3.7
                    elif avg_10 >= 7.0:
                        gpa4 = 3.3
                    elif avg_10 >= 6.5:
                        gpa4 = 3.0
                    elif avg_10 >= 5.5:
                        gpa4 = 2.5
                    elif avg_10 >= 4.0:
                        gpa4 = 2.0
                    else:
                        gpa4 = 0.0
                    student.gpa_4 = gpa4

                    if gpa4 >= 3.5:
                        student.academic_performance = 'excellent'
                    elif gpa4 >= 3.0:
                        student.academic_performance = 'good'
                    elif gpa4 >= 2.5:
                        student.academic_performance = 'fair'
                    elif gpa4 >= 2.0:
                        student.academic_performance = 'average'
                    else:
                        student.academic_performance = 'weak'
                else:
                    student.gpa_4 = student.average_10 = 0.0
                    student.academic_performance = 'weak'
            else:
                student.gpa_4 = student.average_10 = 0.0
                student.academic_performance = 'weak'

