from openerp import models, api, fields

class ProdTempl(models.Model):
    _inherit = 'product.template'

    @api.multi
    def write(self, vals):
        if not 'pack' in vals:
            vals['pack'] = self.pack
        # print vals
        if 'pack' in vals and vals['pack'] == True:
            vals['type'] = 'service'
        return super(ProdTempl, self).write(vals)

    @api.model
    def create(self,vals):
        if vals['pack'] == True:
            vals['type'] = 'service'
        return super(ProdTempl, self).create(vals)
