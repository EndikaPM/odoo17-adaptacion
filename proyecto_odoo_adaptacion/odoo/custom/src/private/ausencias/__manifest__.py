{
    "name": "ausencias",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """Modulo para gestionar ausencas en odoo""",
    "author": "Endika Perez",
    "website": "https://www.yourcompany.com",

    "category": "Uncategorized",
    "version": "0.1",

    "depends": ["base", "hr", "hr_empleados_practica"],

    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
        "report/consulta_horas_views.xml",
        "report/consulta_horas_report_template.xml",
        "report/consulta_solicitudes_report_template.xml",
        "report/consulta_solicitudes_views.xml",
    ],

    "demo": [
        "demo/demo.xml",
    ],
}
