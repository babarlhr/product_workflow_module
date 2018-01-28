from odoo import models, fields, api
from lxml import etree
from odoo.tools.safe_eval import safe_eval
from odoo.osv.orm import setup_modifiers
# from odoo.api import model

class PurchaseOrderLineCustom(models.Model):
    _inherit = 'purchase.order.line'
    
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True),('state','=','approved')], change_default=True, required=True)
    
class SaleOrderLineCustom(models.Model):
    _inherit = 'sale.order.line'
    
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True),('state','=','approved')], change_default=True, ondelete='restrict', required=True)

class product_template(models.Model):
    _inherit = 'product.template'
    _description = 'This model adds workflow states to the product product model'
    
    state = fields.Selection([('draft', 'Draft'),('approved','Approved')], default="draft")
    
    def action_approve(self):
        self.state = 'approved'
        
    def action_reset(self):
        self.state = 'draft'
        
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(product_template, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type=="form":
            doc = etree.XML(result['arch'])
            for node in doc.iter(tag="field"):
                if 'readonly' in node.attrib.get("modifiers",''):
                    attrs = node.attrib.get("attrs",'')
                    if 'readonly' in attrs:
                        attrs_dict = safe_eval(node.get('attrs'))
                        r_list = attrs_dict.get('readonly',)
                        if type(r_list)==list:
                            r_list.insert(0,('state','=','approved'))
                            if len(r_list)>1:
                                r_list.insert(0,'|')
                        attrs_dict.update({'readonly':r_list})
                        node.set('attrs', str(attrs_dict))
                        setup_modifiers(node, result['fields'][node.get("name")])
                        continue
                    else:
                        continue
                node.set('attrs', "{'readonly':[('state','=','approved')]}")
                setup_modifiers(node, result['fields'][node.get("name")])
                
            result['arch'] = etree.tostring(doc)
        return result