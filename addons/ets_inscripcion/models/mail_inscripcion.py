from odoo import models


def _template_inscripcion(env):
    return env.ref('ets_inscripcion.mail_template_inscripcion', raise_if_not_found=False)


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def send_mail(self, res_ids, *args, **kwargs):
        result = super().send_mail(res_ids, *args, **kwargs)
        tmpl = _template_inscripcion(self.env)
        if tmpl and tmpl in self and tmpl.model == 'crm.lead':
            if isinstance(res_ids, models.BaseModel):
                leads = res_ids
            else:
                ids = res_ids if isinstance(res_ids, (list, tuple)) else [res_ids]
                leads = self.env['crm.lead'].browse(ids)
            leads._ets_move_to_informacion_enviada()
        return result


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def _action_send_mail(self, *args, **kwargs):
        tmpl = _template_inscripcion(self.env)
        lead_ids = []
        for wizard in self:
            if not tmpl or not wizard.template_id or wizard.template_id.id != tmpl.id:
                continue
            model = wizard.res_model or getattr(wizard, 'model', None)
            if model != 'crm.lead':
                continue
            if hasattr(wizard, '_evaluate_res_ids'):
                lead_ids.extend(wizard._evaluate_res_ids() or [])
            elif wizard.res_id:
                lead_ids.append(wizard.res_id)
        result = super()._action_send_mail(*args, **kwargs)
        if lead_ids:
            self.env['crm.lead'].browse(lead_ids)._ets_move_to_informacion_enviada()
        return result
