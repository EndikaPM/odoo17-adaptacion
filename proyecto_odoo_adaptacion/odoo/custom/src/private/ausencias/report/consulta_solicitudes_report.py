"""Controlador del reporte PDF de solicitudes de ausencia."""
from odoo import api, fields, models
class ReportConsultaSolicitudes(models.AbstractModel):
    _name = "report.ausencias.report_consulta_solicitudes"
    _description = "Reporte PDF: Solicitudes de Ausencia"
    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env["ausencias.consulta.solicitudes"]
        docs = model.browse(docids) if docids else model.search([])
        rows = []
        for r in docs:
            rows.append({
                "id": r.id,
                "nombre": r.nombre,
                "tipo_motivo": r.tipo_motivo,
                "fecha_inicio": r.fecha_inicio,
                "fecha_fin": r.fecha_fin,
                "hora_inicio": r.hora_inicio,
                "hora_fin": r.hora_fin,
                "dias_solicitados": r.dias_solicitados,
            })
        total_dias = sum(r["dias_solicitados"] for r in rows)
        return {
            "doc_ids": docs.ids,
            "doc_model": "ausencias.consulta.solicitudes",
            "docs": docs,
            "rows": rows,
            "total_dias": total_dias,
            "total_solicitudes": len(rows),
            "generated_at": fields.Datetime.now(),
        }
