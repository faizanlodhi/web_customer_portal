# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
import logging
from odoo import exceptions, SUPERUSER_ID
import base64
import werkzeug.utils
from werkzeug.utils import secure_filename


_logger = logging.getLogger(__name__)


class Main(http.Controller):

    @http.route('/users', type='http', auth="user", website=True)
    def get_all_users(self):
        return request.render(
            'customer_portal.partners', {
                'partners': request.env['res.partner'].search([]),
            })

    @http.route('/users/<model("res.partner"):partner>', type='http', auth="user", website=True)
    def partner_book_detail(self, partner):
        return request.render(
            'customer_portal.partner_detail', {
                'partner': partner,
                'main_object': partner
            })

    @http.route('/submit_contact_form', type='http', auth='public', methods=['POST'], csrf=False)
    def submit_contact_form(self, **post):
        name = post.get('name')
        email = post.get('email')
        message = post.get('message')
        attachment = request.httprequest.files.get('attachment')
        partner_id = int(post.get('partner_id'))
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner:
            attachment_id = False
            if attachment:
                filename = werkzeug.utils.secure_filename(attachment.filename)
                attachment_data = base64.b64encode(attachment.read()).decode('utf-8')
                attachment_record = request.env['ir.attachment'].sudo().create({
                    'name': filename,
                    'datas': attachment_data,
                    'db_datas': True,
                    'res_model': 'res.partner',
                    'res_id': partner_id,
                    'type': 'binary',
                })
                attachment_id = attachment_record.id
            message_vals = {
                'body': message,
                'subject': "Message from Website Contact Form",
                'message_type': 'comment',
                'subtype_xmlid': 'mail.mt_comment',
                'email_from': email,
                'author_id': partner_id,
            }
            if attachment_id:
                message_vals['attachment_ids'] = (4 , attachment_id)
            partner.message_post(**message_vals)
            return redirect('/partner_detail/%s' % partner_id)
        else:
            return redirect('/partner_detail/%s?error=1' % partner_id)

    @http.route('/partner_detail/<int:partner_id>', type='http', auth='public', website=True)
    def partner_detail(self, partner_id, **kwargs):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        error = 'error' in kwargs
        return request.render('customer_portal.partner_detail', {
            'partner': partner,
            'error': error
        })

    @http.route('/partner_login', type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=False)
    def partner_login(self, **post):
        if request.httprequest.method == 'POST':
            username = post.get('username')
            password = post.get('password')
            if username and password:
                partner = request.env['res.partner'].sudo().search([('username', '=', username)], limit=1)
                if partner and partner.password == password:
                    return redirect(f'/partner_detail/{partner.id}')
                else:
                    return request.render('customer_portal.log_in', {'error': 'Invalid username or password'})
        return request.render('customer_portal.log_in')

    @http.route('/partner_logout', type='http', auth='public', website=True)
    def partner_logout(self):
        request.session.pop('partner_id', None)
        return request.redirect('/')

    @http.route('/download/invoice/<int:invoice_id>', type='http', auth='public', website=True)
    def download_invoice(self, invoice_id, **kwargs):
        _logger.info(f"Attempting to download invoice with ID: {invoice_id}")
        invoice = request.env['account.move'].sudo().browse(invoice_id)
        if not invoice:
            return request.not_found()
        pdf, _ = request.env.ref('account.account_invoices').with_user(SUPERUSER_ID)._render_qweb_pdf([invoice.id])
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', f'attachment; filename=invoice_{invoice.name}.pdf')
        ]
        _logger.info(f"Successfully generated PDF for invoice ID: {invoice_id}")
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route('/custom/download/attachment/<int:attachment_id>', type='http', auth='public', website=True)
    def download_attachment(self, attachment_id, **kwargs):
        _logger.info(f"Attempting to download attachment with ID: {attachment_id}")
        attachment = request.env['ir.attachment'].sudo().browse(attachment_id)
        if not attachment:
            return request.not_found()
        headers = [
            ('Content-Type', attachment.mimetype),
            ('Content-Disposition', f'attachment; filename={attachment.name}')
        ]
        return request.make_response(attachment.datas, headers=headers)
