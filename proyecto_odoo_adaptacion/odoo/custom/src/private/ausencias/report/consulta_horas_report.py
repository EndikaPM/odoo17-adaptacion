"""Controlador de reportes personalizados para ausencias."""

from odoo import api, fields, models


class ReportConsultaHoras(models.AbstractModel):
    _name = "report.ausencias.report_consulta_horas"
    _description = "Reporte PDF: Horas por Empleado"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Prepara los datos para la plantilla QWEB del reporte.

        Args:
            docids: IDs de registros a reportar
            data: datos adicionales del wizard (si los hay)

        Returns:
            dict con los datos que recibirá la plantilla QWEB
        """
        # Obtenemos todos los registros de la consulta de horas
        consulta_horas = self.env["ausencias.consulta.horas"].search([])

        # Procesamos cada fila para añadir estilos condicionales
        rows = []
        for row in consulta_horas:
            row_data = {
                "id": row.id,
                "nombre": row.nombre,
                "dni": row.dni,
                "horas_contrato_anual": row.horas_contrato_anual,
                "horas_contrato_mes": row.horas_contrato_mes,
                "horas_trabajadas": row.horas_trabajadas,
                "horas_extra": row.horas_extra,
                # Clase CSS según horas extra (verde si debe, rojo si tiene extras)
                "extra_style": "green" if row.horas_extra <= 0 else "red",
                "extra_label": "Debe"
                if row.horas_extra < 0
                else "OK"
                if row.horas_extra == 0
                else "Extras",
            }
            rows.append(row_data)

        return {
            "doc_model": "ausencias.consulta.horas",
            "rows": rows,
            "total_extras": sum(r["horas_extra"] for r in rows),
            "total_debe": sum(r["horas_extra"] for r in rows if r["horas_extra"] < 0),
            "generated_at": fields.Datetime.now(),
        }
