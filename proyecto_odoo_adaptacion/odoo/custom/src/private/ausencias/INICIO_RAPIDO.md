# 🚀 Guía de Inicio Rápido - API de Ausencias

## 5 Minutos para Empezar

### Paso 1: Reinicia Odoo
```bash
# Si usas docker
cd /home/endika/odoo17-adaptacion/proyecto_odoo_adaptacion
docker-compose restart
```

### Paso 2: Verifica que funciona
```bash
# Prueba rápida
curl http://localhost:8069/api/ausencias/opciones-tipo-motivo
```

Deberías ver:
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

### Paso 3: En tu React, usa estos endpoints

#### Obtener todas las ausencias:
```javascript
fetch('http://localhost:8069/api/ausencias/listar')
    .then(r => r.json())
    .then(data => console.log(data.data))
```

#### Crear una ausencia:
```javascript
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
.then(data => {
    if (data.success) {
        console.log('Creada con ID:', data.ausencia.id)
    }
})
```

---

## 📍 3 Endpoints Disponibles

```
GET  /api/ausencias/listar
GET  /api/ausencias/opciones-tipo-motivo
POST /api/ausencias/crear
```

---

## 🎨 Componente React Mínimo

```javascript
import { useState, useEffect } from 'react';

export function AusenciasForm() {
    const [mensaje, setMensaje] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        const formData = {
            fecha_inicio: e.target.fecha_inicio.value,
            fecha_fin: e.target.fecha_fin.value,
            tipo_motivo: e.target.tipo_motivo.value,
            descripcion_motivo: e.target.descripcion_motivo.value
        };

        fetch('http://localhost:8069/api/ausencias/crear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                setMensaje(`✅ Ausencia creada: ${data.ausencia.id}`);
                e.target.reset();
            } else {
                setMensaje(`❌ Error: ${data.error}`);
            }
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="date" name="fecha_inicio" required />
            <input type="date" name="fecha_fin" required />

            <select name="tipo_motivo" defaultValue="VACACIONES">
                <option value="VACACIONES">Vacaciones</option>
                <option value="MEDICO">Médico</option>
                <option value="ASUNTOS">Asuntos Propios</option>
                <option value="OTROS">Otros</option>
            </select>

            <textarea name="descripcion_motivo" required />

            <button type="submit">Crear Ausencia</button>
            {mensaje && <p>{mensaje}</p>}
        </form>
    );
}
```

---

## 📊 Tipo Motivo - Opciones

| Valor | Etiqueta |
|-------|----------|
| `VACACIONES` | Vacaciones |
| `MEDICO` | Médico |
| `ASUNTOS` | Asuntos Propios |
| `OTROS` | Otros |

---

## 🔧 Campos Requeridos vs Opcionales

✅ **Requeridos:**
- `fecha_inicio` (YYYY-MM-DD)
- `fecha_fin` (YYYY-MM-DD)
- `tipo_motivo` (ver opciones arriba)
- `descripcion_motivo` (texto descriptivo)

⭕ **Opcionales:**
- `hora_inicio` (decimal: 9.0 = 9:00 AM)
- `hora_fin` (decimal: 17.0 = 5:00 PM)
- `employee_id` (se infiere si está logueado)

---

## ✨ Ejemplo de Respuesta Exitosa

### Crear ausencia:
```json
{
    "success": true,
    "message": "Ausencia creada exitosamente",
    "ausencia": {
        "id": 15,
        "employee_id": 5,
        "employee_name": "Juan Pérez",
        "fecha_inicio": "2024-05-15",
        "hora_inicio": 8.0,
        "fecha_fin": "2024-05-17",
        "hora_fin": 17.0,
        "tipo_motivo": "VACACIONES",
        "descripcion_motivo": "Vacaciones"
    }
}
```

### Listar ausencias:
```json
{
    "success": true,
    "data": [
        {...},
        {...}
    ],
    "count": 2
}
```

---

## ⚠️ Errores Comunes

### Error: Fecha en el pasado
```json
{"success": false, "error": "No se pueden crear ausencias en el pasado"}
```

### Error: tipo_motivo inválido
```json
{
    "success": false,
    "error": "tipo_motivo inválido. Debe ser uno de: VACACIONES, MEDICO, ASUNTOS, OTROS"
}
```

### Error: Conexión rechazada
- ¿Está Odoo corriendo en `localhost:8069`?
- Cambia la URL en el código si es necesario

---

## 🧪 Probar con cURL

```bash
# Listar
curl http://localhost:8069/api/ausencias/listar | jq

# Crear
curl -X POST http://localhost:8069/api/ausencias/crear \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_inicio":"2024-05-20",
    "fecha_fin":"2024-05-22",
    "tipo_motivo":"MEDICO",
    "descripcion_motivo":"Cita al doctor"
  }' | jq
```

---

## 📦 Usando Python

```bash
pip install requests
```

```python
import requests

# Listar
r = requests.get('http://localhost:8069/api/ausencias/listar')
print(r.json())

# Crear
data = {
    "fecha_inicio": "2024-05-25",
    "fecha_fin": "2024-05-26",
    "tipo_motivo": "ASUNTOS",
    "descripcion_motivo": "Asuntos"
}
r = requests.post('http://localhost:8069/api/ausencias/crear', json=data)
print(r.json())
```

---

## 🐛 Debugging

### Ver logs de Odoo:
```bash
docker logs -f proyecto_odoo_adaptacion_odoo_1
```

### Verificar el módulo está instalado:
```bash
# En Odoo:
# Aplicaciones → Busca "ausencias" → Debe estar en VERDE
```

### Probar con REST Client (VS Code):
```http
GET http://localhost:8069/api/ausencias/listar
Content-Type: application/json
```

---

## 📚 Documentación Completa

- **README.md** - Resumen general
- **API_DOCUMENTATION.md** - Docs completas
- **EJEMPLOS_SOLICITUDES.md** - Ejemplos de prueba
- **SEGURIDAD_CONFIGURACION.md** - Seguridad y CORS

---

## ✅ Checklist Rápido

- [ ] Odoo corriendo
- [ ] Módulo ausencias instalado
- [ ] `curl http://localhost:8069/api/ausencias/opciones-tipo-motivo` funciona
- [ ] React puede hacer fetch a `/api/ausencias/listar`
- [ ] React puede POST a `/api/ausencias/crear`
- [ ] Datos aparecen en Odoo

**¡Listo! 🎉**

