{
    "name": "HR Empleados Práctica",
    "version": "17.0.1.0.0",
    "category": "Human Resources",
    "summary": "Campos personalizados para empleados: DNI, fecha nacimiento, seguridad social, horas, etc.",
    "description": """
        Módulo de práctica que hereda del módulo hr (Empleados) de Odoo.
        Añade campos personalizados al modelo hr.employee:
        - Fecha de nacimiento (x_fecha_nacimiento)
        - Contraseña (x_contrasena)
        - DNI (x_dni)
        - Fecha de contratación (x_fecha_contratacion)
        - Número de seguridad social (x_num_seg_social)
        - Horas contratadas (x_horas_contratado)
        - Horas trabajadas (x_horas_trabajadas)
        - Horas extra (x_horas_extra) - campo calculado
    """,
    "author": "Endika - Práctica 2º DAM",
    "website": "",
    "license": "LGPL-3",
    "depends": ["hr"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
