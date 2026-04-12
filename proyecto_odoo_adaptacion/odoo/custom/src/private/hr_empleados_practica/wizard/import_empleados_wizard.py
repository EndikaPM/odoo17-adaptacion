import base64
import csv
import io

import xlrd  # para .xls

from odoo import _, fields, models
from odoo.exceptions import UserError


class ImportEmpleadosWizard(models.TransientModel):
    _name = "import.empleados.wizard"
    _description = "Importar Empleados desde CSV/XLS"

    file = fields.Binary(string="Archivo", required=True)
    file_name = fields.Char(string="Nombre del archivo")

    def action_importar(self):
        if not self.file:
            raise UserError(_("Por favor, selecciona un archivo."))

        nombre = (self.file_name or "").lower()

        if nombre.endswith(".csv"):
            self._importar_csv()
        elif nombre.endswith(".xls") or nombre.endswith(".xlsx"):
            self._importar_xls()
        else:
            raise UserError(_("Formato no soportado. Usa .csv o .xls/.xlsx"))

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Importación completada"),
                "message": _("Los empleados se han importado correctamente."),
                "type": "success",
                "sticky": False,
            },
        }

    def _parse_row(self, row):
        """Recibe un dict con las claves del CSV/XLS y crea/actualiza el empleado."""
        Empleado = self.env["hr.employee"]

        name = row.get("name", "").strip()
        if not name:
            return

        dni = (row.get("dni") or "").strip()

        vals = {
            "name": name,
            "x_es_timely": True,
        }

        if row.get("fecha_de_nacimiento"):
            vals["x_fecha_nacimiento"] = row.get("fecha_de_nacimiento")
        if row.get("num_seg_social"):
            vals["x_num_seg_social"] = (row.get("num_seg_social") or "").strip()

        # Campos personalizados (asegúrate de que existen en tu modelo)
        if dni:
            vals["x_dni"] = dni
        if row.get("fecha_contratacion"):
            vals["x_fecha_contratacion"] = row["fecha_contratacion"]
        if row.get("horas_trabajadas"):
            vals["x_horas_trabajadas"] = float(row["horas_trabajadas"] or 0)
        if row.get("horas_contrato"):
            vals["x_horas_contratado"] = float(row["horas_contrato"] or 0)

        tag = self.env["hr.employee.category"].search(
            [("name", "=", "Timely")], limit=1
        )
        if not tag:
            tag = self.env["hr.employee.category"].create({"name": "Timely"})
        vals["category_ids"] = [(4, tag.id)]

        # Buscar por DNI para evitar duplicados
        if dni:
            empleado = Empleado.search([("x_dni", "=", dni)], limit=1)
        else:
            empleado = Empleado.search([("name", "=", name)], limit=1)
        if empleado:
            empleado.write(vals)
        else:
            empleado = Empleado.create(vals)

        # Contraseña: si quieres vincularla al usuario relacionado
        if row.get("password") and empleado.user_id:
            empleado.user_id.password = row["password"].strip()

    def _importar_csv(self):
        contenido = base64.b64decode(self.file)
        texto = contenido.decode("utf-8-sig")  # utf-8-sig maneja el BOM de Excel
        reader = csv.DictReader(io.StringIO(texto))
        for fila in reader:
            self._parse_row(fila)

    def _importar_xls(self):
        contenido = base64.b64decode(self.file)
        libro = xlrd.open_workbook(file_contents=contenido)
        hoja = libro.sheet_by_index(0)
        cabeceras = [hoja.cell_value(0, c) for c in range(hoja.ncols)]
        for r in range(1, hoja.nrows):
            fila = {cabeceras[c]: hoja.cell_value(r, c) for c in range(hoja.ncols)}
            self._parse_row(fila)
