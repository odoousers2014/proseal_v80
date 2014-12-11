from openerp.osv import fields, osv

class res_partner(osv.osv):
    _inherit    = "res.partner"
    _columns    = {
                   'customer_number'                : fields.char('Customer Number',size=64),
                   'supplier_number'                : fields.char('Supplier Number',size=64),
                   'customer_outstanding_balance'   : fields.float('Customer Outstanding Balance'),
                   'gst_hst_reg_no'                 : fields.char('GST/HST Registration Number',size=64),
                   'pst_reg_no'                     : fields.char('PST Registration Number',size=64),
                   'ship_via'                       : fields.char('Ship Via',size=64),
                   }