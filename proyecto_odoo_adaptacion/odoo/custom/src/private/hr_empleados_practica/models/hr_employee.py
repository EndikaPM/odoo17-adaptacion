from odoo import api, fields, models


class HrEmployee(models.Model):
    """Herencia del modelo hr.employee para añadir campos personalizados."""

    _inherit = "hr.employee"

    # --- Timely ---
    x_es_timely = fields.Boolean(
        string="Empleado Timely",
        default=False,
        help="Marca este empleado como perteneciente a Timely. "
             "Al activarlo se asigna automáticamente la etiqueta 'Timely'.",
    )

    @api.onchange("x_es_timely")
    def _onchange_es_timely(self):
        """Al marcar/desmarcar el checkbox, añade o quita la etiqueta 'Timely'."""
        tag = self.env["hr.employee.category"].search(
            [("name", "=", "Timely")], limit=1
        )
        if not tag:
            tag = self.env["hr.employee.category"].create({"name": "Timely"})
        if self.x_es_timely:
            self.category_ids = [(4, tag.id)]  # 4 = añadir sin borrar los demás
        else:
            self.category_ids = [(3, tag.id)]  # 3 = quitar sin borrar los demás

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
