from openerp.osv import osv,fields
class stock_picking_out(osv.osv):
    _inherit = "stock.picking.out"
    _description = "Delivery Orders"
    _columns        = {
                        'state': fields.selection(
                            [('draft', 'Draft'),
                            ('auto', 'Waiting Another Operation'),
                            ('confirmed', 'Waiting Availability'),
                            ('partial','Partially Available'),
                            ('assigned', 'Ready to Deliver'),
                            ('done', 'Delivered'),
                            ('cancel', 'Cancelled'),],
                            'Status', readonly=True, select=True,
                            help="""* Draft: not confirmed yet and will not be scheduled until confirmed\n
                                 * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n
                                 * Waiting Availability: still waiting for the availability of products\n
                                 * Ready to Deliver: products reserved, simply waiting for confirmation.\n
                                 * Delivered: has been processed, can't be modified or cancelled anymore\n
                                 * Cancelled: has been cancelled, can't be confirmed anymore"""),
                       }
    def create_chained_picking(self,cr,uid,ids,context=None):
        return super(stock_picking_out,self).create_chained_picking(cr,uid,ids,context=None)
    
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms stock move.
        @return: List of ids.
        """
        print "NEW STATE"
        moves = self.browse(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'state': 'confirmed'})
        self.create_chained_picking(cr, uid, moves, context)
        for move in moves:
            for line in move.move_lines:
                print line.state
        return []
    
class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns        = {
                        'state': fields.selection(
                            [('draft', 'Draft'),
                            ('auto', 'Waiting Another Operation'),
                            ('confirmed', 'Waiting Availability'),
                            ('partial','Partially Available'),
                            ('assigned', 'Ready to Deliver'),
                            ('done', 'Delivered'),
                            ('cancel', 'Cancelled'),],
                            'Status', readonly=True, select=True,
                            help="""* Draft: not confirmed yet and will not be scheduled until confirmed\n
                                 * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n
                                 * Waiting Availability: still waiting for the availability of products\n
                                 * Ready to Deliver: products reserved, simply waiting for confirmation.\n
                                 * Delivered: has been processed, can't be modified or cancelled anymore\n
                                 * Cancelled: has been cancelled, can't be confirmed anymore"""),
                       }
    def action_partial(self, cr, uid, ids, context=None):
        """ Confirms picking.
        @return: True
        """
        pickings = self.browse(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'state': 'partial'})
        todo = []
        for picking in pickings:
            for r in picking.move_lines:
                if r.state == 'draft':
                    todo.append(r.id)
        todo = self.pool.get('stock.picking').action_explode(cr, uid, todo, context)
        if len(todo):
            self.pool.get('stock.move').action_confirm(cr, uid, todo, context=context)
        return True
    def test_partial(self,cr,uid,ids):
        print "TEST PARTIAL"
        ok = False
        for pick in self.browse(cr,uid,ids):
            mt = pick.move_type
            if pick.type == 'in':
                if all([x.state != 'waiting' for x in pick.move_lines]):
                    return True
            for move in pick.move_lines:
                print "Move Lines", move.name, move.state
                if (mt == 'direct') and (move.state == 'confirmed') and (move.product_qty):
                    return True
                ok = ok and (move.state in ('confirmed'))
        print "Partial",ok
        return ok
    def test_assigned(self, cr, uid, ids):
        """ Tests whether the move is in assigned state or not.
        @return: True or False
        """
        #TOFIX: assignment of move lines should be call before testing assigment otherwise picking never gone in assign state
        ok = True
        for pick in self.browse(cr, uid, ids):
            mt = pick.move_type
            # incomming shipments are always set as available if they aren't chained
            if pick.type == 'in':
                if all([x.state != 'waiting' for x in pick.move_lines]):
                    return True
            for move in pick.move_lines:
                if (move.state in ('confirmed', 'draft')) and (mt == 'one'):
                    return False
                if (mt == 'direct') and (move.state == 'assigned') and (move.product_qty):
                    return True
                ok = ok and (move.state in ('cancel', 'done', 'assigned'))
        return ok
    