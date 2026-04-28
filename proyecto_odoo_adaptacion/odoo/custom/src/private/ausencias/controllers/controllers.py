import json
from odoo import http
from odoo.http import request


class AusenciasAPI(http.Controller):
    """Controlador API para gestionar ausencias desde aplicaciones externas (React, etc)"""

    @http.route('/api/ausencias/listar', auth='public', type='http', methods=['GET'], csrf=False)
    def listar_ausencias(self):
        """
        Retorna todas las ausencias almacenadas en formato JSON
        GET /api/ausencias/listar
        """
        try:
            ausencias = request.env['ausencias.solicitudes'].search([])

            ausencias_data = []
            for ausencia in ausencias:
                ausencias_data.append({
                    'id': ausencia.id,
                    'employee_id': ausencia.employee_id.id if ausencia.employee_id else None,
                    'employee_name': ausencia.employee_id.name if ausencia.employee_id else None,
                    'fecha_inicio': ausencia.fecha_inicio.isoformat() if ausencia.fecha_inicio else None,
                    'hora_inicio': ausencia.hora_inicio,
                    'fecha_fin': ausencia.fecha_fin.isoformat() if ausencia.fecha_fin else None,
                    'hora_fin': ausencia.hora_fin,
                    'tipo_motivo': ausencia.tipo_motivo,
                    'descripcion_motivo': ausencia.descripcion_motivo,
                })

            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': ausencias_data,
                    'count': len(ausencias_data)
                }),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'error': str(e)
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )

    @http.route('/api/ausencias/crear', auth='public', type='json', methods=['POST'], csrf=False)
    def crear_ausencia(self):
        """
        Crea una nueva ausencia desde un JSON
        POST /api/ausencias/crear

        Datos esperados en el body (JSON):
        {
            "employee_id": 1,  (opcional - si no viene se usa del contexto del usuario)
            "fecha_inicio": "2024-04-27",
            "hora_inicio": 9.0,  (opcional)
            "fecha_fin": "2024-05-01",
            "hora_fin": 17.0,  (opcional)
            "tipo_motivo": "VACACIONES",
            "descripcion_motivo": "Descripción de la ausencia"
        }
        """
        try:
            data = request.get_json_data()

            # Validaciones básicas
            if not data.get('fecha_inicio'):
                return {'success': False, 'error': 'fecha_inicio es requerido'}
            if not data.get('fecha_fin'):
                return {'success': False, 'error': 'fecha_fin es requerido'}
            if not data.get('tipo_motivo'):
                return {'success': False, 'error': 'tipo_motivo es requerido'}
            if not data.get('descripcion_motivo'):
                return {'success': False, 'error': 'descripcion_motivo es requerido'}

            # Validar que tipo_motivo sea válido
            valid_tipos = ['VACACIONES', 'MEDICO', 'ASUNTOS', 'OTROS']
            if data['tipo_motivo'] not in valid_tipos:
                return {
                    'success': False,
                    'error': f"tipo_motivo inválido. Debe ser uno de: {', '.join(valid_tipos)}"
                }

            # Si no viene employee_id, usar el empleado del usuario actual
            employee_id = data.get('employee_id')
            if not employee_id:
                current_user = request.env.user
                employee = request.env['hr.employee'].search([('user_id', '=', current_user.id)], limit=1)
                if employee:
                    employee_id = employee.id
                else:
                    return {'success': False, 'error': 'No se pudo determinar el empleado. Proporcione employee_id'}

            # Crear la ausencia
            ausencia_vals = {
                'employee_id': employee_id,
                'fecha_inicio': data['fecha_inicio'],
                'fecha_fin': data['fecha_fin'],
                'tipo_motivo': data['tipo_motivo'],
                'descripcion_motivo': data['descripcion_motivo'],
                'hora_inicio': data.get('hora_inicio', 0),
                'hora_fin': data.get('hora_fin', 0),
            }

            nueva_ausencia = request.env['ausencias.solicitudes'].create(ausencia_vals)

            return {
                'success': True,
                'message': 'Ausencia creada exitosamente',
                'ausencia': {
                    'id': nueva_ausencia.id,
                    'employee_id': nueva_ausencia.employee_id.id,
                    'employee_name': nueva_ausencia.employee_id.name,
                    'fecha_inicio': nueva_ausencia.fecha_inicio.isoformat(),
                    'hora_inicio': nueva_ausencia.hora_inicio,
                    'fecha_fin': nueva_ausencia.fecha_fin.isoformat(),
                    'hora_fin': nueva_ausencia.hora_fin,
                    'tipo_motivo': nueva_ausencia.tipo_motivo,
                    'descripcion_motivo': nueva_ausencia.descripcion_motivo,
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/api/ausencias/opciones-tipo-motivo', auth='public', type='http', methods=['GET'], csrf=False)
    def obtener_opciones_tipo_motivo(self):
        """
        Retorna las opciones disponibles para tipo_motivo
        GET /api/ausencias/opciones-tipo-motivo
        """
        try:
            opciones = [
                {"value": "VACACIONES", "label": "Vacaciones"},
                {"value": "MEDICO", "label": "Médico"},
                {"value": "ASUNTOS", "label": "Asuntos Propios"},
                {"value": "OTROS", "label": "Otros"},
            ]

            return request.make_response(
                json.dumps({
                    'success': True,
                    'data': opciones
                }),
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'error': str(e)
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
