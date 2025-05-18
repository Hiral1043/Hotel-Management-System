from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class HousekeepingReportIssue(models.Model):
    _name = 'housekeeping.report.issue'
    _description = 'Housekeeping Report Issue'
    _rec_name = 'issue_type'

    guest_name = fields.Many2one('hotel.guest', string="Guest Name")
    hotel_id = fields.Many2one('hotel.hotel', string="Hotel")
    room_id = fields.Many2one('hotel.rooms', string="Room")
    issue_type = fields.Char(string="Issue Type", required=True)
    issue_description = fields.Text(string="Issue Description")
    issue_date = fields.Date(string="Issue Date", default=fields.Date.today())
    status = fields.Selection([('reported', 'Reported'),
                                ('resolved', 'Resolved')], 
                                string="Status", default='reported')
    maintainance_type_id = fields.Many2one('housekeeping.maintainance.type', string="Maintainance Type")
    solved_by = fields.Many2one('hotel.housekeeping.staff', string="Solved By")
    solved_date = fields.Date(string="Solved Date")
    solution = fields.Text(string="Solution")

    def action_report_issue(self):
        self.status = 'reported'
        
    def action_solve_issue(self):
        if not self.solved_by:
            raise ValidationError("Please select a staff member who solved the issue.")
        if not self.solution:
            raise ValidationError("Please provide a solution for the issue.")
        self.status = 'resolved'
        self.solved_date = fields.Date.today()
        