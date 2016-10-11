from openerp import models, fields, api
from datetime import datetime, timedelta
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class hr_analytic_timesheet_improvements(models.Model):
    _inherit = 'account.analytic.line'

    def _get_default_date(self):
        return datetime.strftime(self.check_and_correct_date_in_fifteen_step(datetime.now()), '%Y-%m-%d %H:%M:%S')

    date_begin = fields.Datetime(string='Start Date', default=_get_default_date)
    
    def check_and_correct_date_in_fifteen_step(self, date):
        newdate = date
        newhour = newdate.hour
        step = 0
        round = False
        minute_under_fifteen = newdate.minute
        while (minute_under_fifteen > 15):
           minute_under_fifteen = minute_under_fifteen - 15
           step+=1
        if(minute_under_fifteen>=(15/2)):
            round = True
        if round:
            newminute = (step*15)+15
            if newminute==60:
                newdate = newdate + timedelta(hours=1)
                newminute = 0
        else:
            newminute = step*15
        
        newdate = newdate.replace(minute=newminute, second=0)
        return newdate

    # set the date of date_begin to "date" to avoid consistency problems
    @api.multi
    @api.onchange('date_begin')
    def copy_dates(self):
        self.date = self.date_begin

    @api.model
    def create(self, vals):
        hr_analytic_timesheet_id = super(hr_analytic_timesheet_improvements, self).create(vals)

        # Test if timesheet or not
        if hr_analytic_timesheet_id.sheet_id:
            hr_analytic_timesheet_id.is_timesheet = True
            if hr_analytic_timesheet_id.date_begin:
                start_date = datetime.strptime(hr_analytic_timesheet_id.date_begin, '%Y-%m-%d %H:%M:%S')
                newdate = self.check_and_correct_date_in_fifteen_step(start_date)
                if start_date.minute != newdate.minute or start_date.second != newdate.second:
                    hr_analytic_timesheet_id.date_begin = datetime.strftime(self.check_and_correct_date_in_fifteen_step(start_date), '%Y-%m-%d %H:%M:%S')
            else:
                hr_analytic_timesheet_id.date_begin = datetime.strftime(self.check_and_correct_date_in_fifteen_step(datetime.now()), '%Y-%m-%d %H:%M:%S')
        return hr_analytic_timesheet_id

    @api.multi
    def write(self, values):
        result = super(hr_analytic_timesheet_improvements, self).write(values)
        for timesheet in self:
            if timesheet.date_begin:
                start_date = datetime.strptime(timesheet.date_begin, '%Y-%m-%d %H:%M:%S')
                newdate = self.check_and_correct_date_in_fifteen_step(start_date)
                if start_date.minute != newdate.minute or start_date.second != newdate.second:
                    timesheet.date_begin = datetime.strftime(newdate, '%Y-%m-%d %H:%M:%S')
            else:
                timesheet.date_begin = datetime.strftime(self.check_and_correct_date_in_fifteen_step(datetime.now()), '%Y-%m-%d %H:%M:%S')
        return result

    def _set_date_begin_if_date_exits(self, cr, uid, ids=None, context=None):
        hr_analytic_timesheet_obj = self.pool.get('account.analytic.line')
        hr_analytic_timesheets = hr_analytic_timesheet_obj.search(cr, uid, [('date', 'like', '-')])
        if hr_analytic_timesheets:
            for hr_analytic_timesheet in hr_analytic_timesheet_obj.browse(cr, uid, hr_analytic_timesheets):
                if hr_analytic_timesheet.date:
                    begin_date = datetime.strftime(datetime.strptime(hr_analytic_timesheet.date, '%Y-%m-%d').replace(hour=0,minute=0, second=0), '%Y-%m-%d %H:%M:%S')
                    query = """
                            UPDATE account_analytic_line
                            SET date_begin=%s
                            WHERE id=%s
                            """
                    cr.execute(query, (begin_date,hr_analytic_timesheet.id))
