{
    "name"          : "Proseal Custom Delivery",
    "version"       : "1.0",
    "depends"       : ["stock"],
    "author"        : "Togar Hutabarat",
    "description"   : """This module is aim to add new state on Delivery Order that indicates availability for partial shipment.""",
    "website"       : "https://www.odesk.com/users/~014ecb73724f396338",
    "category"      : "Warehouse",
    "init_xml"      : [],
    "demo_xml"      : [],
    'test'          : [],
    "update_xml"    : [
                       "stock_view.xml",
                       "stock_workflow.xml"
                       ],
    "active"        : False,
    "installable"   : True,
}