from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class GymSubscriptionPlan(models.Model):
    _name = 'gym.subscription.plan'
    _description = 'Gym Subscription Plan'

    name = fields.Char(string='Plan Name', required=True)
    duration_value = fields.Integer(string='Duration', required=True, default=1)
    duration_unit = fields.Selection([
        ('day', 'Day(s)'),
        ('week', 'Week(s)'),
        ('month', 'Month(s)'),
        ('year', 'Year(s)')
    ], string='Duration Unit', required=True, default='month')
    price = fields.Monetary(string='Price', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Subscription plan name must be unique!'),
    ]

class GymSubscription(models.Model):
    _name = 'gym.subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Gym Member Subscription'

    name = fields.Char(string='Subscription Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    member_id = fields.Many2one('gym.member', string='Member', required=True, tracking=True)
    plan_id = fields.Many2one('gym.subscription.plan', string='Subscription Plan', required=True, tracking=True)
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today(), tracking=True)
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True, tracking=True)
    price = fields.Monetary(string='Price', related='plan_id.price', currency_field='currency_id', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='plan_id.currency_id', store=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Payment'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False)
    payment_status = fields.Selection(related='invoice_id.payment_state', string='Payment Status', readonly=True, store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('gym.subscription.sequence') or _('New')
        subscription = super(GymSubscription, self).create(vals)
        return subscription

    @api.depends('start_date', 'plan_id.duration_value', 'plan_id.duration_unit')
    def _compute_end_date(self):
        for sub in self:
            if sub.start_date and sub.plan_id:
                if sub.plan_id.duration_unit == 'day':
                    sub.end_date = sub.start_date + relativedelta(days=sub.plan_id.duration_value)
                elif sub.plan_id.duration_unit == 'week':
                    sub.end_date = sub.start_date + relativedelta(weeks=sub.plan_id.duration_value)
                elif sub.plan_id.duration_unit == 'month':
                    sub.end_date = sub.start_date + relativedelta(months=sub.plan_id.duration_value)
                elif sub.plan_id.duration_unit == 'year':
                    sub.end_date = sub.start_date + relativedelta(years=sub.plan_id.duration_value)
            else:
                sub.end_date = False

    def action_confirm_subscription(self):
        self.ensure_one()
        if not self.plan_id:
            raise ValidationError(_("Please select a subscription plan first."))
        # Create invoice
        invoice_line_vals = {
            'name': f"{self.plan_id.name} Subscription for {self.member_id.name}",
            'quantity': 1,
            'price_unit': self.price,
            'account_id': self.env['account.account'].search([
                ('account_type', '=', 'income'),
                ('company_ids', '=', self.env.company.id)
            ], limit=1).id
        }
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.member_id.user_id.partner_id.id if self.member_id.user_id and self.member_id.user_id.partner_id else self.member_id.partner_id.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': [(0, 0, invoice_line_vals)],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id
        self.state = 'pending'

    def action_confirm_subscription(self):
        self.ensure_one()

        if not self.plan_id:
            raise ValidationError(_("Please select a subscription plan first."))

        # Search account
        income_account = self.env['account.account'].search([
            ('account_type', '=', 'income'),
            ('company_ids', '=', self.env.company.id)
        ], limit=1)
        if not income_account:
            raise ValidationError(_("No income account found. Please configure your chart of accounts."))

        # Invoice lines prepare
        invoice_line_vals = {
            'name': f"{self.plan_id.name} Subscription for {self.member_id.name}",
            'quantity': 1,
            'price_unit': self.price,
            'account_id': income_account.id,
        }

        #  Create a member-linked partner
        partner = None
        if self.member_id.user_id and self.member_id.user_id.partner_id:
            partner = self.member_id.user_id.partner_id
        else:
            partner = self.env['res.partner'].create({
                'name': self.member_id.name,
                'email': self.member_id.email,
                'phone': self.member_id.phone,
            })

        # Invoice data
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, invoice_line_vals)],
            'company_id': self.env.company.id,
        }

        invoice = self.env['account.move'].create(invoice_vals)

        # Invoice link 
        self.invoice_id = invoice.id
        self.state = 'pending'

        return {
            'name': _("Invoice"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current',
        }

    def action_cancel_subscription(self):
        self.ensure_one()
        self.state = 'cancelled'
        if self.invoice_id and self.invoice_id.state == 'draft':
            self.invoice_id.button_cancel() # Cancel draft invoice

    def action_set_active(self):
        self.ensure_one()
        if self.invoice_id and self.invoice_id.payment_state == 'paid':
            self.state = 'active'
        else:
            raise ValidationError(_("Subscription cannot be set to active without a paid invoice."))

    @api.model
    def _cron_check_expired_subscriptions(self):
        """ Cron job to check and update expired subscriptions """
        today = fields.Date.today()
        expired_subscriptions = self.search([
            ('state', '=', 'active'),
            ('end_date', '<', today)
        ])
        for sub in expired_subscriptions:
            sub.state = 'expired'
            sub.message_post(body=_("Subscription has expired."))

