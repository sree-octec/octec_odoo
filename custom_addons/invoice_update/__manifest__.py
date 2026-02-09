{
    "name": "Invoice Multi-level Approval",
    "author": "Octec",
    "license": "LGPL-3",
    "version": "18.0.1.1",
    "summary": "Add two approval levels for customer invoices",
    "depends": ["base", "account"],
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "views/account_move_views.xml"
    ],
    "application": True,
    "installable": True,
}
