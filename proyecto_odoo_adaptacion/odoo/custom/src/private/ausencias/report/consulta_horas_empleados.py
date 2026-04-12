"""
Consultas / Reportes de Ausencias
==================================
Aquí se definen las consultas SQL que alimentan las vistas de reportes.
Para añadir una nueva consulta, crea una clase con _auto = False
y define su vista SQL en el método init().

CONSULTA 1 – Horas por empleado (mes actual)
---------------------------------------------
Muestra: nombre, DNI, horas contrato anual, horas contrato mensual
         (anual / 12), horas trabajadas este mes, y horas extra
         (trabajadas − contrato mensual).
"""

from odoo import fields, models, tools


class ConsultaHorasEmpleados(models.Model):
    _name = "ausencias.consulta.horas"
    _description = "Consulta: Horas de Empleados"
    _auto = False  # No crea tabla real → usa la vista SQL de init()
    _order = "nombre"
    _rec_name = "nombre"

    # ------------------------------------------------------------------
    # Campos (deben coincidir con las columnas del SELECT en init())
    # ------------------------------------------------------------------
    nombre = fields.Char(string="Nombre", readonly=True)
    dni = fields.Char(string="DNI", readonly=True)
    horas_contrato_anual = fields.Float(
        string="Horas Contrato Anual",
        readonly=True,
    )
    horas_contrato_mes = fields.Float(
        string="Horas Contrato / Mes",
        readonly=True,
        help="Horas contrato anual divididas entre 12.",
    )
    horas_trabajadas = fields.Float(
        string="Horas Trabajadas",
        readonly=True,
    )
    horas_extra = fields.Float(
        string="Horas Extra",
        readonly=True,
        help="Horas trabajadas − horas contrato mensual. "
        "Negativo = debe horas; positivo = extras.",
    )

    # ------------------------------------------------------------------
    # Vista SQL  –  MODIFICA AQUÍ la lógica si lo necesitas
    # ------------------------------------------------------------------
    def init(self):
        """Crea (o reemplaza) la vista SQL que alimenta este modelo.

        Fórmulas actuales
        -----------------
        · horas_contrato_mes  = x_horas_contratado / 12
        · horas_extra         = x_horas_trabajadas − horas_contrato_mes

        Si en el futuro quieres dividir por el nº del mes actual en vez
        de 12, cambia el «12» por:
            EXTRACT(MONTH FROM CURRENT_DATE)
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                -- ============================================================
                -- CONSULTA: Horas por empleado
                -- Devuelve: nombre, DNI, horas contrato anual,
                --           horas contrato mensual, horas trabajadas, horas extra
                -- ============================================================

                SELECT
                    -- ID único del empleado (clave primaria de la vista)
                    e.id                                           AS id,

                    -- Nombre completo del empleado
                    e.name                                         AS nombre,

                    -- DNI del empleado (campo personalizado x_dni)
                    e.x_dni                                        AS dni,

                    -- Horas contratadas ANUALES (tal como está en la BD)
                    -- COALESCE = si es NULL, usa 0 para evitar errores
                    COALESCE(e.x_horas_contratado, 0)              AS horas_contrato_anual,

                    -- Horas contratadas MENSUALES = anual / 12
                    -- ROUND = redondea a 2 decimales
                    -- ::numeric = convierte a tipo numérico para ROUND
                    ROUND(
                        (COALESCE(e.x_horas_contratado, 0) / 12.0)::numeric,
                        2
                    )                                              AS horas_contrato_mes,

                    -- Horas realmente TRABAJADAS este mes
                    COALESCE(e.x_horas_trabajadas, 0)              AS horas_trabajadas,

                    -- HORAS EXTRA = Horas trabajadas - Horas contrato mensual
                    -- Si es POSITIVO = ha trabajado EXTRAS
                    -- Si es NEGATIVO = debe horas (trabajó menos)
                    ROUND(
                        (COALESCE(e.x_horas_trabajadas, 0)
                        - COALESCE(e.x_horas_contratado, 0) / 12.0)::numeric,
                        2
                    )                                             AS horas_extra

                -- Se obtienen datos de la tabla hr_employee (empleados)
                FROM hr_employee e

                -- Solo empleados ACTIVOS (no desactivados/despedidos)
                WHERE e.active = true
            )
        """
            % self._table
        )
