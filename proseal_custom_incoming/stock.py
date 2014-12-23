from openerp.osv import osv,fields
from openerp.tools.translate import _

class stock_move(osv.osv):
    _inherit        = "stock.move"
    
    def set_supplier_product(self,cr,uid,ids,name,args,context=None):
        res = {}
        for m in self.browse(cr,uid,ids,context=None):
            if not m.picking_id.partner_id:
                res[m.id] = False
                return res

            sp_ids = self.pool.get('product.supplierinfo').search(cr,uid,[('product_tmpl_id','=',m.product_id.product_tmpl_id.id),('name','=',m.picking_id.partner_id.id)])
            if sp_ids:
                res[m.id] = sp_ids[0]
            else:
                res[m.id] = False
        return res
    
    def get_move_by_picking(self,cr,uid,ids,context=None):
        move_ids = []
        if ids:
            move_ids = self.pool.get('stock.move').search(cr,uid,[('picking_id','=',ids[0])])
            print move_ids
        return move_ids
    
    def get_move_by_move(self,cr,uid,ids,context=None):
        return ids
    
    def get_move_by_supplierinfo(self,cr,uid,ids,context=None):
        return True
    
    _columns        = {
                       'supplier_product_id'    : fields.function(set_supplier_product, type='many2one',
                                                  relation='product.supplierinfo', string='Product Supplier Info',
                                                  store={
                                                         'stock.picking': (get_move_by_picking,['partner_id'],10),
                                                         'stock.move': (get_move_by_move,['product_id'],10),
#                                                          'product.supplierinfo': (get_move_by_supplierinfo,['product_name','product_code'],None,10)
                                                         }
                                                  )
                       }

class product_supplierinfo(osv.osv):
    _inherit        = "product.supplierinfo"
    
    def name_get(self, cr, uid, ids, context=None):
        res = []
        for si in self.browse(cr, uid, ids, context=context):
            name = '[%s] %s' % (si.product_code or 'N/A',si.product_name or 'N/A')
            res.append((si.id, name))
        return res
    