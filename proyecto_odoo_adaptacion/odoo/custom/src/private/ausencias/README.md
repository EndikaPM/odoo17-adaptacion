# API de Ausencias - Resumen de Implementación

## 🎯 Objetivo

Crear una API para conectar el módulo de ausencias de Odoo 17 con una aplicación React, permitiendo:
- ✅ Obtener todas las ausencias almacenadas en formato JSON
- ✅ Crear nuevas ausencias desde la aplicación React
- ✅ Obtener las opciones válidas para tipo_motivo

---

## 📦 Lo que se implementó

### 1. **API Endpoints** (en `controllers/controllers.py`)

#### GET `/api/ausencias/listar`
Retorna todas las ausencias almacenadas en formato JSON

**Respuesta:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "employee_id": 5,
            "employee_name": "Juan Pérez",
            "fecha_inicio": "2024-04-27",
            "fecha_fin": "2024-05-01",
            "tipo_motivo": "VACACIONES",
            "descripcion_motivo": "Vacaciones de primavera"
        }
    ],
    "count": 1
}
```

#### POST `/api/ausencias/crear`
Crea una nueva ausencia desde JSON

**Datos esperados:**
```json
{
    "fecha_inicio": "2024-05-10",
    "fecha_fin": "2024-05-17",
    "tipo_motivo": "VACACIONES",
    "descripcion_motivo": "Descripción de la ausencia"
}
```

#### GET `/api/ausencias/opciones-tipo-motivo`
Retorna las opciones disponibles para tipo_motivo

**Respuesta:**
```json
{
    "success": true,
    "data": [
        {"value": "VACACIONES", "label": "Vacaciones"},
        {"value": "MEDICO", "label": "Médico"},
        {"value": "ASUNTOS", "label": "Asuntos Propios"},
        {"value": "OTROS", "label": "Otros"}
    ]
}
```

---

## 📁 Archivos Creados/Modificados

### 1. **controllers/controllers.py** (✏️ Modificado)
- Implementa 3 endpoints REST
- Manejo completo de errores
- Validaciones de datos
- Respuestas en formato JSON

### 2. **API_DOCUMENTATION.md** (📄 Nuevo)
Documentación completa del API con:
- Descripción de cada endpoint
- Ejemplos de uso con fetch
- Ejemplo de app React completa
- Guía de solución de problemas

### 3. **EJEMPLOS_SOLICITUDES.md** (📄 Nuevo)
Ejemplos prácticos para probar la API:
- Comandos cURL
- Configuración para Postman
- Scripts de prueba en Node.js y Python
- Ejemplos de respuestas

### 4. **client_ausencias_api.py** (📄 Nuevo)
Cliente Python reutilizable:
- Clase `AusenciasAPIClient` para consumir la API
- Métodos helper para cada tipo de motivo
- Filtrado por empleado, tipo de motivo, fechas
- Ejecutable con ejemplos

### 5. **SEGURIDAD_CONFIGURACION.md** (📄 Nuevo)
Guía de configuración y seguridad:
- Configuración de CORS
- Mejoras de autenticación
- Validaciones adicionales
- Rate limiting
- Logging y auditoría
- Testing
- Checklist de seguridad

---

## 🚀 Cómo Usar

### Desde React

```javascript
// 1. Obtener opciones
fetch('http://localhost:8069/api/ausencias/opciones-tipo-motivo')
    .then(r => r.json())
    .then(data => console.log(data.data))

// 2. Listar ausencias
fetch('http://localhost:8069/api/ausencias/listar')
    .then(r => r.json())
    .then(data => console.log(data.data))

// 3. Crear ausencia
fetch('http://localhost:8069/api/ausencias/crear', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        fecha_inicio: '2024-05-15',
        fecha_fin: '2024-05-17',
        tipo_motivo: 'VACACIONES',
        descripcion_motivo: 'Mi descripción'
    })
})
.then(r => r.json())
.then(data => console.log(data))
```

### Desde Python

```python
from client_ausencias_api import AusenciasAPIClient

client = AusenciasAPIClient()

# Listar todas las ausencias
ausencias = client.list_ausencias()

# Crear una vacación
resultado = client.create_vacaciones(
    fecha_inicio="2024-06-01",
    fecha_fin="2024-06-07",
    descripcion="Vacaciones de verano",
    employee_id=5
)
```

### Desde cURL

```bash
# Listar
curl http://localhost:8069/api/ausencias/listar

# Crear
curl -X POST http://localhost:8069/api/ausencias/crear \
  -H "Content-Type: application/json" \
  -d '{"fecha_inicio":"2024-05-15","fecha_fin":"2024-05-17","tipo_motivo":"VACACIONES","descripcion_motivo":"Test"}'
```

---

## ⚙️ Configuración

### Pasos de instalación:

1. **Reiniciar Odoo** (para que cargue el código actualizado)
   ```bash
   # Si usas docker
   docker-compose restart
   ```

2. **Activar el módulo** (si está desactivado)
   - Ve a Aplicaciones → Busca "ausencias"
   - Instala el módulo

3. **Verificar que funciona**
   ```bash
   curl http://localhost:8069/api/ausencias/opciones-tipo-motivo
   ```

### Para CORS (si React está en otro dominio):

Consulta la sección "Configuración de CORS" en `SEGURIDAD_CONFIGURACION.md`

---

## 📋 Campos de la Ausencia

| Campo | Tipo | Requerido | Descripción |
|-------|------|----------|-------------|
| `employee_id` | Integer | No* | ID del empleado (opcional si está autenticado) |
| `fecha_inicio` | String (YYYY-MM-DD) | Sí | Fecha de inicio de la ausencia |
| `hora_inicio` | Float | No | Hora de inicio (formato decimal, ej: 9.0) |
| `fecha_fin` | String (YYYY-MM-DD) | Sí | Fecha de fin de la ausencia |
| `hora_fin` | Float | No | Hora de fin |
| `tipo_motivo` | String | Sí | VACACIONES, MEDICO, ASUNTOS, OTROS |
| `descripcion_motivo` | String | Sí | Descripción detallada |

---

## 🔒 Seguridad (Importante)

La API actualmente es **pública** (`auth='public'`). Para producción:

1. **Cambiar a `auth='user'`** en controllers.py
2. **Implementar autenticación** (consulta `SEGURIDAD_CONFIGURACION.md`)
3. **Agregar validaciones** adicionales
4. **Implementar rate limiting**
5. **Configurar HTTPS**

---

## 🧪 Testing

### Con Postman:
1. Importa la colección desde `EJEMPLOS_SOLICITUDES.md`
2. Prueba cada endpoint

### Con Python:
```bash
# Ejecutar el script de prueba
python /path/to/client_ausencias_api.py
```

### Con Node.js:
```bash
cd /home/endika/odoo17-adaptacion/proyecto_odoo_adaptacion/odoo/custom/src/private/ausencias
node test-api.js  # (script del archivo EJEMPLOS_SOLICITUDES.md)
```

---

## 📚 Documentación Disponible

- **API_DOCUMENTATION.md** - Documentación completa y ejemplos en React
- **EJEMPLOS_SOLICITUDES.md** - Ejemplos con cURL, Postman, Python, Node.js
- **SEGURIDAD_CONFIGURACION.md** - Guía de seguridad, CORS, autenticación
- **client_ausencias_api.py** - Cliente Python ejecutable con ejemplos

---

## ❓ Preguntas Frecuentes

### ¿Cómo manejo CORS?
→ Ver sección "Configuración de CORS" en `SEGURIDAD_CONFIGURACION.md`

### ¿Necesito autenticación?
→ Actualmente no, pero se recomienda para producción. Ver guía de seguridad.

### ¿Qué formato de horas?
→ Decimal: 9.0 = 9:00 AM, 14.5 = 14:30, etc.

### ¿Puedo filtrar ausencias?
→ Sí, mira los métodos del cliente Python (`get_ausencias_by_employee`, etc.)

### ¿Supuso cambios en el modelo?
→ No, los endpoints funcionan con el modelo existente.

---

## 🐛 Solución de Problemas

### Error: "Connection refused"
- Verifica que Odoo esté corriendo en `localhost:8069`
- Cambia la URL a la correcta si es necesario

### Error: "CORS policy"
- La aplicación React y Odoo están en dominios diferentes
- Configura CORS (ver guía en `SEGURIDAD_CONFIGURACION.md`)

### Error: "employee_id no encontrado"
- Proporciona un `employee_id` válido
- O asegúrate de estar autenticado

### Error: "tipo_motivo inválido"
- Usa uno de los valores válidos: VACACIONES, MEDICO, ASUNTOS, OTROS

---

## 📞 Soporte

Para más información:
- Consulta los archivos .md en el directorio del módulo
- Revisa los ejemplos de código en `client_ausencias_api.py`
- Mira los ejemplos de solicitudes en `EJEMPLOS_SOLICITUDES.md`

---

## ✅ Checklist para empezar

- [ ] Reiniciar Odoo
- [ ] Verificar que el módulo ausencias esté instalado
- [ ] Probar un GET a `/api/ausencias/opciones-tipo-motivo`
- [ ] Probar un GET a `/api/ausencias/listar`
- [ ] Probar un POST a `/api/ausencias/crear` con datos válidos
- [ ] Integrar en tu aplicación React
- [ ] Configurar CORS si es necesario
- [ ] For producción: implementar autenticación

---

**¡La API está lista para usar!** 🎉

