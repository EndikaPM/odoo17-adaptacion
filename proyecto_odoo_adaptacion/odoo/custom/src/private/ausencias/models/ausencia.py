from odoo import fields, models


class ausencias(models.Model):
    _name = "ausencias.solicitudes"
    _description = "Solicitudes de Ausencias"

    # relacion con el empleado que solicita la ausencia.
    employee_id = fields.Many2one(
        "hr.employee",
        string="Empleado",
        ondelete="set null",
    )

    # fecha de inicio dela ausencia
    fecha_inicio = fields.Date(string="Fecha de Inicio", required=True)
    # hora de inicio de la ausencia
    hora_inicio = fields.Float(string="Hora de Inicio")

    fecha_fin = fields.Date(string="Fecha de Fin", required=True)
    hora_fin = fields.Float(string="Hora de Fin")

    # Motivo con selección y texto
    tipo_motivo = fields.Selection(
        [
            ("VACACIONES", "Vacaciones"),
            ("MEDICO", "Médico"),
            ("ASUNTOS", "Asuntos Propios"),
            ("OTROS", "Otros"),
        ],
        string="Tipo de Motivo",
        default="VACACIONES",
    )

    descripcion_motivo = fields.Text(string="Explicación detallada", required=True)
