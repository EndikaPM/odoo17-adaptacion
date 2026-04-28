# Guía de Seguridad y Configuración - API de Ausencias

## 1. Configuración de CORS

Si tu aplicación React está en un dominio diferente a Odoo (ej: http://localhost:3000), necesitarás configurar CORS.

### Opción A: Usando middleware en los controladores (Recomendado)

Modifica `/home/endika/odoo17-adaptacion/proyecto_odoo_adaptacion/odoo/custom/src/private/ausencias/controllers/controllers.py` agregando el siguiente código al inicio del archivo:

```python
from flask import make_response

def _cors_response():
    """Agrega headers CORS a las respuestas"""
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response
```

Luego, en los methods de rutas, antes de retornar, asegúrate de incluir headers CORS.

### Opción B: Configuración global en Odoo

Edita el archivo `common.yaml` o `devel.yaml` en la raíz y agrega:

```yaml
options:
  cors_headers:
    - "Content-Type"
    - "Authorization"
```

### Opción C: Cliente React con proxy

En `package.json` de tu proyecto React, agrega:

```json
{
  "proxy": "http://localhost:8069"
}
```

Entonces en React usarías `fetch('/api/ausencias/listar')` en lugar de la URL completa.

---

## 2. Mejorar Seguridad de la API

### Cambiar autenticación de PUBLIC a USER

Para que solo usuarios autenticados puedan crear/listar ausencias:

En `controllers.py`, cambia los decoradores de ruta:

```python
# De esto:
@http.route('/api/ausencias/listar', auth='public', type='http', methods=['GET'], csrf=False)

# A esto:
@http.route('/api/ausencias/listar', auth='user', type='http', methods=['GET'], csrf=False)
```

Pero esto requeriría que desde React envíes las cookies de sesión:

```javascript
fetch('http://localhost:8069/api/ausencias/listar', {
    method: 'GET',
    credentials: 'include',  // Incluir cookies
    headers: {
        'Content-Type': 'application/json',
    }
})
```

### Usar tokens JWT

Para una seguridad más robusta, implementa autenticación con tokens JWT:

Crea un archivo `auth_token.py` en el módulo:

```python
import secrets
import base64
from datetime import datetime, timedelta
from odoo import models, fields, api

class AuthToken(models.Model):
    _name = 'ausencias.auth_token'
    _description = 'Token de autenticación para API'

    token = fields.Char(string='Token', unique=True, required=True)
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    created_at = fields.Datetime(string='Creado en', default=fields.Datetime.now)
    expires_at = fields.Datetime(string='Expira en')
    is_active = fields.Boolean(string='Activo', default=True)

    @api.model
    def generate_token(self, employee_id):
        """Genera un token único para un empleado"""
        token = secrets.token_urlsafe(32)
        expires_at = fields.Datetime.now() + timedelta(days=30)

        auth_token = self.create({
            'token': token,
            'employee_id': employee_id,
            'expires_at': expires_at,
            'is_active': True
        })
        return token

    @api.model
    def validate_token(self, token):
        """Valida un token"""
        auth_token = self.search([
            ('token', '=', token),
            ('is_active', '=', True),
            ('expires_at', '>', fields.Datetime.now())
        ], limit=1)
        return auth_token
```

---

## 3. Validación de Datos

Las validaciones actuales son básicas. Considera agregar:

### Validaciones adicionales en el modelo `ausencia.py`:

```python
from odoo import fields, models, api
from datetime import date

class ausencias(models.Model):
    _name = "ausencias.solicitudes"

    # ...campos existentes...

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        """Valida que fecha_fin sea posterior a fecha_inicio"""
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                if record.fecha_fin < record.fecha_inicio:
                    raise models.ValidationError(
                        "La fecha de fin debe ser posterior a la fecha de inicio"
                    )

    @api.constrains('hora_inicio', 'hora_fin')
    def _check_horas(self):
        """Valida que hora_fin sea posterior a hora_inicio"""
        for record in self:
            if record.hora_inicio and record.hora_fin:
                if record.fecha_inicio == record.fecha_fin:
                    if record.hora_fin <= record.hora_inicio:
                        raise models.ValidationError(
                            "La hora de fin debe ser posterior a la hora de inicio"
                        )
```

### Validación en la API - Mejorar el archivo `controllers.py`:

```python
from datetime import datetime

def _validar_fechas(fecha_inicio, fecha_fin):
    """Valida que las fechas sean válidas"""
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        if fin <= inicio:
            return False, "fecha_fin debe ser posterior a fecha_inicio"

        # Validar que no estén en el pasado
        if inicio < date.today():
            return False, "No se pueden crear ausencias en el pasado"

        return True, None
    except ValueError:
        return False, "Formato de fecha inválido (use YYYY-MM-DD)"
```

---

## 4. Logging y Auditoría

Agrega logs para auditoría:

```python
import logging

_logger = logging.getLogger(__name__)

class AusenciasAPI(http.Controller):

    @http.route('/api/ausencias/crear', auth='public', type='json', methods=['POST'], csrf=False)
    def crear_ausencia(self):
        try:
            data = request.get_json_data()

            _logger.info(
                f"Intento de crear ausencia: empleado={data.get('employee_id')}, "
                f"tipo={data.get('tipo_motivo')}, "
                f"periodo={data.get('fecha_inicio')} a {data.get('fecha_fin')}"
            )

            # ...resto del código...

            _logger.info(f"Ausencia creada exitosamente. ID: {nueva_ausencia.id}")

        except Exception as e:
            _logger.error(f"Error al crear ausencia: {str(e)}", exc_info=True)
            return {'success': False, 'error': str(e)}
```

---

## 5. Rate Limiting

Para evitar abuso de la API, implementa rate limiting:

Crea un archivo `rate_limit.py`:

```python
from time import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, calls=100, period=3600):  # 100 llamadas por hora
        self.calls = calls
        self.period = period
        self.clock = time
        self.calls_made = defaultdict(list)

    def is_allowed(self, identifier):
        """Verifica si la solicitud está permitida"""
        now = self.clock()

        # Limpiar llamadas antiguas
        self.calls_made[identifier] = [
            call_time for call_time in self.calls_made[identifier]
            if call_time > now - self.period
        ]

        # Verificar límite
        if len(self.calls_made[identifier]) < self.calls:
            self.calls_made[identifier].append(now)
            return True

        return False

# Uso en controllers.py
limiter = RateLimiter(calls=100, period=3600)

@http.route('/api/ausencias/crear', auth='public', type='json', methods=['POST'], csrf=False)
def crear_ausencia(self):
    # Obtener identificador (IP del cliente)
    client_id = request.httprequest.remote_addr

    if not limiter.is_allowed(client_id):
        return {'success': False, 'error': 'Límite de solicitudes excedido'}, 429

    # ...resto del código...
```

---

## 6. Versionado de API

Para facilitar cambios futuros, versiona tu API:

```python
# Cambiar rutas de:
@http.route('/api/ausencias/listar', ...)

# A:
@http.route('/api/v1/ausencias/listar', ...)
```

---

## 7. Documentación Swagger/OpenAPI

Para documentar mejor tu API, considera usar Swagger:

```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
```

---

## 8. Manejo de Errores Mejorado

Define códigos de error estandarizados:

```python
ERROR_CODES = {
    'INVALID_TIPO_MOTIVO': 400,
    'MISSING_REQUIRED_FIELD': 400,
    'INVALID_DATE_FORMAT': 400,
    'EMPLOYEE_NOT_FOUND': 404,
    'AUSENCIA_NOT_FOUND': 404,
    'INTERNAL_ERROR': 500,
    'RATE_LIMIT_EXCEEDED': 429,
}

def error_response(code, message, status=400):
    return {
        'success': False,
        'error_code': code,
        'error_message': message
    }, status
```

---

## 9. Testing de la API

Crea un archivo de tests en Python:

`test_ausencias_api.py`:

```python
import unittest
import requests
import json
from datetime import datetime, timedelta

class TestAusenciasAPI(unittest.TestCase):
    BASE_URL = 'http://localhost:8069'

    def test_listar_ausencias(self):
        """Test: Listar ausencias"""
        response = requests.get(f'{self.BASE_URL}/api/ausencias/listar')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('data', data)
        self.assertIn('count', data)

    def test_obtener_opciones(self):
        """Test: Obtener opciones de tipo_motivo"""
        response = requests.get(f'{self.BASE_URL}/api/ausencias/opciones-tipo-motivo')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertEqual(len(data.get('data', [])), 4)

    def test_crear_ausencia_valida(self):
        """Test: Crear ausencia con datos válidos"""
        mañana = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        semana_proxima = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

        payload = {
            'fecha_inicio': mañana,
            'fecha_fin': semana_proxima,
            'tipo_motivo': 'VACACIONES',
            'descripcion_motivo': 'Test vacaciones',
            'employee_id': 5
        }

        response = requests.post(
            f'{self.BASE_URL}/api/ausencias/crear',
            json=payload
        )
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('ausencia', data)
        self.assertIn('id', data['ausencia'])

    def test_crear_ausencia_sin_fecha_inicio(self):
        """Test: Crear ausencia sin fecha_inicio (debe fallar)"""
        payload = {
            'fecha_fin': '2024-05-20',
            'tipo_motivo': 'VACACIONES',
            'descripcion_motivo': 'Test',
            'employee_id': 5
        }

        response = requests.post(
            f'{self.BASE_URL}/api/ausencias/crear',
            json=payload
        )
        data = response.json()
        self.assertFalse(data.get('success'))
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
```

Ejecutar tests:
```bash
python -m unittest test_ausencias_api.py
```

---

## Checklist de Seguridad

- [ ] Validar todas las entradas
- [ ] Usar HTTPS en producción
- [ ] Implementar autenticación
- [ ] Implementar autorización (solo tu empleado puede ver sus ausencias)
- [ ] Agregar rate limiting
- [ ] Implementar logging y auditoría
- [ ] Usar CSRF tokens si es necesario
- [ ] Validar formato de fechas
- [ ] Sanitizar inputs
- [ ] Documentar endpoints
- [ ] Hacer tests
- [ ] Monitorear performance
- [ ] Backup regular de datos

---

## Recomendaciones para Producción

1. **Cambiar auth de 'public' a 'user'**
2. **Implementar HTTPS obligatorio**
3. **Agregar autenticación con tokens**
4. **Implementar rate limiting**
5. **Agregar logging exhaustivo**
6. **Validar todas las entradas**
7. **Usar variables de entorno para configuraciones sensibles**
8. **Implementar monitoreo y alertas**
9. **Hacer backups regulares**
10. **Documentar completamente la API**

