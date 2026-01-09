from odoo import models, fields, api

class Grade(models.Model):
    _name = 'school.grade'
    _description = 'Điểm môn học'
    _rec_name = 'subject_id'
    enrollment_id = fields.Many2one(
        'school.enrollment',
        string='Đăng ký',
        required=True,
        ondelete='cascade')
    student_id = fields.Many2one(
        'school.student',
        related='enrollment_id.student_id',
        store=True,
        readonly=True,
        string='Sinh viên')
    subject_id = fields.Many2one(
        'school.subject',
        related='enrollment_id.subject_id',
        store=True,
        readonly=True,
        string='Môn học')
    semester_id = fields.Many2one(
        'school.semester',
        related='enrollment_id.semester_id',
        store=True,
        readonly=True,
        string='Học kỳ')
    teacher_id = fields.Many2one(
        'school.teacher',
        related='enrollment_id.teacher_id',
        store=True,
        readonly=True,
        string='Giảng viên')
    attendance_score = fields.Float(string='Điểm chuyên cần (10%)', digits=(3, 1), default=0.0)
    midterm_score = fields.Float(string='Điểm giữa kỳ (30%)', digits=(3, 1), default=0.0)
    final_score = fields.Float(string='Điểm cuối kỳ (60%)', digits=(3, 1), default=0.0)
    total_score = fields.Float(
        string='Điểm tổng kết',
        compute='_compute_total',
        store=True,
        digits=(3, 1))
    result = fields.Selection([
        ('pass', 'Đạt'),
        ('fail', 'Không đạt')
    ], string='Kết quả', compute='_compute_result', store=True)
    @api.depends('attendance_score', 'midterm_score', 'final_score')
    def _compute_total(self):
        for grade in self:
            grade.total_score = (
                (grade.attendance_score or 0) * 0.1 +
                (grade.midterm_score or 0) * 0.3 +
                (grade.final_score or 0) * 0.6
            )
    @api.depends('total_score')
    def _compute_result(self):
        for grade in self:
            grade.result = 'pass' if grade.total_score >= 5.0 else 'fail'