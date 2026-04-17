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
        # Si no se pasan ids, el reporte incluye todos los empleados.
        consulta_horas_model = self.env["ausencias.consulta.horas"]
        consulta_horas = (
            consulta_horas_model.browse(docids)
            if docids
            else consulta_horas_model.search([])
        )

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

        total_mas = sum(r["horas_extra"] for r in rows if r["horas_extra"] > 0)
        total_menos = abs(sum(r["horas_extra"] for r in rows if r["horas_extra"] < 0))
        total_neto = sum(r["horas_extra"] for r in rows)

        return {
            "doc_ids": consulta_horas.ids,
            "doc_model": "ausencias.consulta.horas",
            "docs": consulta_horas,
            "rows": rows,
            "total_mas": total_mas,
            "total_menos": total_menos,
            "total_neto": total_neto,
            "generated_at": fields.Datetime.now(),
        }
