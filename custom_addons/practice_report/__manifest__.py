{
    "name": "Report Custom",
    "version": "1.0.0",
    "licence": "LGPL-3",
    "author": "sreejith vijayakumar",
    "summary": "Report printing",
    "depends": ["base", "resource"],
    "data": [
        "security/ir.model.access.csv",
        "security/security_groups.xml",
        
        "reports/project_detail_report.xml",
        "reports/employee_detail_report.xml",
        "views/project_report.xml",
        "views/practice_project_detail_view.xml",
        "views/employee_report.xml",
        "views/practice_employee_detail_view.xml",
        "views/menu.xml"
    ],
    "application": True,
    "installable": True
    
}