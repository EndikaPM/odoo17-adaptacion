from odoo import api, fields, models


class HrEmployee(models.Model):
    """Herencia del modelo hr.employee para añadir campos personalizados."""

    _inherit = "hr.employee"

    # --- Datos personales ---
    x_fecha_nacimiento = fields.Date(
        string="Fecha de Nacimiento",
        help="Fecha de nacimiento del empleado.",
    )
    x_dni = fields.Char(
        string="DNI",
        size=20,
        help="Documento Nacional de Identidad del empleado.",
    )
    x_contrasena = fields.Char(
        string="Contraseña",
        help="Contraseña interna del empleado (uso administrativo).",
    )

    # --- Datos laborales ---
    x_fecha_contratacion = fields.Date(
        string="Fecha de Contratación",
        help="Fecha en la que el empleado fue contratado.",
    )
    x_num_seg_social = fields.Char(
        string="Nº Seguridad Social",
        size=30,
        help="Número de afiliación a la Seguridad Social.",
    )

    # --- Horas ---
    x_horas_contratado = fields.Float(
        string="Horas Contratadas",
        default=0.0,
        help="Número de horas que tiene contratadas el empleado (mensuales).",
    )
    x_horas_trabajadas = fields.Float(
        string="Horas Trabajadas",
        default=0.0,
        help="Número de horas realmente trabajadas por el empleado (mensuales).",
    )
    x_horas_extra = fields.Float(
        string="Horas Extra",
        compute="_compute_horas_extra",
        store=True,
        help="Horas extra = Horas Trabajadas - Horas Contratadas. "
        "Si es negativo, el empleado ha trabajado menos de lo contratado.",
    )

    @api.depends("x_horas_trabajadas", "x_horas_contratado")
    def _compute_horas_extra(self):
        """Calcula las horas extra como la diferencia entre horas trabajadas
        y horas contratadas. Puede ser negativo si ha trabajado menos."""
        for employee in self:
            employee.x_horas_extra = (
                employee.x_horas_trabajadas - employee.x_horas_contratado
            )
