from odoo import models, api


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    @api.model
    def _ets_apply_stage_order(self):
        """Nuevo (0) → Nuevo TIC (5) → Información Enviada (10) → resto."""
        refs = [
            ('crm.stage_lead1', 0),
            ('ets_inscripcion.stage_nuevo_tic', 5),
            ('crm.stage_lead2', 10),
            ('crm.stage_lead3', 20),
            ('crm.stage_lead4', 30),
        ]
        used = self.env['crm.stage']
        for xmlid, seq in refs:
            stage = self.env.ref(xmlid, raise_if_not_found=False)
            if stage:
                stage.sudo().write({'sequence': seq})
                used |= stage
        extras = self.sudo().search([('id', 'not in', used.ids)], order='sequence, id')
        seq = 40
        for stage in extras:
            stage.write({'sequence': seq})
            seq += 10
