"""
CONSULTA 2 – Solicitudes de ausencia por empleado
---------------------------------------------------
Muestra: nombre empleado, tipo motivo, fecha inicio, fecha fin,
         hora inicio, hora fin y días solicitados (fecha_fin - fecha_inicio + 1).
"""

from odoo import fields, models, tools


class ConsultaSolicitudesEmpleados(models.Model):
    _name = "ausencias.consulta.solicitudes"
    _description = "Consulta: Solicitudes de Ausencia"
    _auto = False
    _order = "fecha_inicio DESC"
    _rec_name = "nombre"

    # ------------------------------------------------------------------
    # Campos (deben coincidir con las columnas del SELECT en init())
    # ------------------------------------------------------------------
    nombre = fields.Char(string="Empleado", readonly=True)
    tipo_motivo = fields.Char(string="Motivo", readonly=True)
    fecha_inicio = fields.Date(string="Fecha Inicio", readonly=True)
    fecha_fin = fields.Date(string="Fecha Fin", readonly=True)
    hora_inicio = fields.Float(string="Hora Inicio", readonly=True)
    hora_fin = fields.Float(string="Hora Fin", readonly=True)
    dias_solicitados = fields.Integer(
        string="Días Solicitados",
        readonly=True,
        help="Número de días naturales entre fecha inicio y fecha fin (ambas incluidas).",
    )

    # ------------------------------------------------------------------
    # Vista SQL
    # ------------------------------------------------------------------
    def init(self):
        """Crea (o reemplaza) la vista SQL que alimenta este modelo.

        Fórmulas
        --------
        · dias_solicitados = fecha_fin − fecha_inicio + 1
          (días naturales, ambas fechas incluidas)

        Tablas
        ------
        · ausencias_solicitudes  → solicitudes de ausencia
        · hr_employee            → nombre del empleado
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                -- ============================================================
                -- CONSULTA: Solicitudes de ausencia por empleado
                -- Devuelve: nombre, motivo, fecha inicio/fin,
                --           hora inicio/fin, días solicitados
                -- ============================================================

                SELECT
                    -- ID único de la solicitud (PK de la vista)
                    s.id AS id,

                    -- Nombre completo del empleado (viene de hr_employee)
                    e.name AS nombre,

                    -- Tipo de motivo tal cual está almacenado
                    -- (VACACIONES, MEDICO, ASUNTOS, OTROS)
                    s.tipo_motivo AS tipo_motivo,

                    -- Fechas de inicio y fin de la solicitud
                    s.fecha_inicio AS fecha_inicio,
                    s.fecha_fin    AS fecha_fin,

                    -- Horas (almacenadas como float en la BD)
                    COALESCE(s.hora_inicio, 0) AS hora_inicio,
                    COALESCE(s.hora_fin, 0)    AS hora_fin,

                    -- DÍAS SOLICITADOS = fecha_fin − fecha_inicio + 1
                    -- Cuenta días naturales, ambas fechas incluidas
                    -- Ejemplo: del 10 al 12 → 12 − 10 + 1 = 3 días
                    (s.fecha_fin - s.fecha_inicio + 1) AS dias_solicitados

                -- Tabla principal: solicitudes de ausencia
                FROM ausencias_solicitudes s

                -- JOIN con hr_employee para obtener el nombre
                LEFT JOIN hr_employee e
                    ON s.employee_id = e.id
            )
        """
            % self._table
        )

