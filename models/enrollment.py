from odoo import models, fields, api

class Enrollment(models.Model):
    _name = 'school.enrollment'
    _description = 'Đăng ký tín chỉ'
    _order = 'student_id, semester_id'
    student_id = fields.Many2one('school.student', string='Sinh viên', required=True)
    subject_id = fields.Many2one('school.subject', string='Môn học', required=True)
    teacher_id = fields.Many2one('school.teacher', string='Giảng viên dạy')
    year_id = fields.Many2one('school.academic.year', string='Năm học', required=True)
    semester_id = fields.Many2one('school.semester', string='Học kỳ', required=True)
    credits = fields.Integer(string='Số tín chỉ', related='subject_id.credits', readonly=True)
    state = fields.Selection([
        ('registered', 'Đăng ký'),
        ('studying', 'Đang học'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Hủy')
    ], string='Trạng thái', default='registered')
    grade_id = fields.Many2one('school.grade', string='Điểm môn học', readonly=True)
    @api.model
    def create(self, vals):
        enrollment = super(Enrollment, self).create(vals)
        if not enrollment.grade_id:
            grade = self.env['school.grade'].create({
                'enrollment_id': enrollment.id,})
            enrollment.grade_id = grade.id
        enrollment.state = 'studying'
        return enrollment

    def write(self, vals):
        result = super(Enrollment, self).write(vals)
        for enrollment in self:
            if enrollment.grade_id:
                if enrollment.grade_id.final_score > 0:
                    enrollment.state = 'completed'
                elif enrollment.grade_id.attendance_score > 0 or enrollment.grade_id.midterm_score > 0:
                    enrollment.state = 'studying'
        return result