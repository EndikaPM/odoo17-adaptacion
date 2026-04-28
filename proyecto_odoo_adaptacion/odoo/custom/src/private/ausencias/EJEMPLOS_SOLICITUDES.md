# Ejemplos de Solicitudes API - cURL y Postman

## RUL Base
```
http://localhost:8069
```

---

## 1. Listar todas las ausencias

### cURL
```bash
curl -X GET "http://localhost:8069/api/ausencias/listar" \
  -H "Content-Type: application/json"
```

### cURL con output formateado
```bash
curl -X GET "http://localhost:8069/api/ausencias/listar" \
  -H "Content-Type: application/json" | jq '.'
```

### Postman
- **Método:** GET
- **URL:** http://localhost:8069/api/ausencias/listar
- **Headers:**
  - Content-Type: application/json

---

## 2. Crear una nueva ausencia

### cURL - Ejemplo 1: Vacaciones
```bash
curl -X POST "http://localhost:8069/api/ausencias/crear" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_inicio": "2024-05-10",
    "fecha_fin": "2024-05-17",
    "tipo_motivo": "VACACIONES",
    "descripcion_motivo": "Vacaciones de primavera",
    "hora_inicio": 8.0,
    "hora_fin": 17.0,
    "employee_id": 5
  }'
```

### cURL - Ejemplo 2: Permiso médico
```bash
curl -X POST "http://localhost:8069/api/ausencias/crear" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_inicio": "2024-05-20",
    "fecha_fin": "2024-05-20",
    "tipo_motivo": "MEDICO",
    "descripcion_motivo": "Cita con el dentista",
    "hora_inicio": 14.0,
    "hora_fin": 15.5,
    "employee_id": 5
  }'
```

### cURL - Ejemplo 3: Asuntos propios
```bash
curl -X POST "http://localhost:8069/api/ausencias/crear" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_inicio": "2024-06-01",
    "fecha_fin": "2024-06-01",
    "tipo_motivo": "ASUNTOS",
    "descripcion_motivo": "Gestiones personales urgentes",
    "hora_inicio": 9.0,
    "hora_fin": 12.0,
    "employee_id": 5
  }'
```

### cURL - Ejemplo 4: Otros
```bash
curl -X POST "http://localhost:8069/api/ausencias/crear" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_inicio": "2024-06-10",
    "fecha_fin": "2024-06-10",
    "tipo_motivo": "OTROS",
    "descripcion_motivo": "Permiso especial solicitado",
    "employee_id": 5
  }'
```

### Postman
- **Método:** POST
- **URL:** http://localhost:8069/api/ausencias/crear
- **Headers:**
  - Content-Type: application/json
- **Body (raw JSON):**
```json
{
    "fecha_inicio": "2024-05-10",
    "fecha_fin": "2024-05-17",
    "tipo_motivo": "VACACIONES",
    "descripcion_motivo": "Vacaciones de primavera",
    "hora_inicio": 8.0,
    "hora_fin": 17.0,
    "employee_id": 5
}
```

---

## 3. Obtener opciones de tipo_motivo

### cURL
```bash
curl -X GET "http://localhost:8069/api/ausencias/opciones-tipo-motivo" \
  -H "Content-Type: application/json"
```

### cURL con output formateado
```bash
curl -X GET "http://localhost:8069/api/ausencias/opciones-tipo-motivo" \
  -H "Content-Type: application/json" | jq '.'
```

### Postman
- **Método:** GET
- **URL:** http://localhost:8069/api/ausencias/opciones-tipo-motivo
- **Headers:**
  - Content-Type: application/json

---

## Ejemplos de Respuestas

### Respuesta exitosa - Listar ausencias
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "employee_id": 5,
      "employee_name": "Juan Pérez García",
      "fecha_inicio": "2024-05-10",
      "hora_inicio": 8.0,
      "fecha_fin": "2024-05-17",
      "hora_fin": 17.0,
      "tipo_motivo": "VACACIONES",
      "descripcion_motivo": "Vacaciones de primavera"
    },
    {
      "id": 2,
      "employee_id": 5,
      "employee_name": "Juan Pérez García",
      "fecha_inicio": "2024-05-20",
      "hora_inicio": 14.0,
      "fecha_fin": "2024-05-20",
      "hora_fin": 15.5,
      "tipo_motivo": "MEDICO",
      "descripcion_motivo": "Cita con el dentista"
    }
  ],
  "count": 2
}
```

### Respuesta exitosa - Crear ausencia
```json
{
  "success": true,
  "message": "Ausencia creada exitosamente",
  "ausencia": {
    "id": 3,
    "employee_id": 5,
    "employee_name": "Juan Pérez García",
    "fecha_inicio": "2024-06-01",
    "hora_inicio": 9.0,
    "fecha_fin": "2024-06-01",
    "hora_fin": 12.0,
    "tipo_motivo": "ASUNTOS",
    "descripcion_motivo": "Gestiones personales urgentes"
  }
}
```

### Respuesta de error - Campo requerido faltante
```json
{
  "success": false,
  "error": "fecha_inicio es requerido"
}
```

### Respuesta de error - tipo_motivo inválido
```json
{
  "success": false,
  "error": "tipo_motivo inválido. Debe ser uno de: VACACIONES, MEDICO, ASUNTOS, OTROS"
}
```

### Respuesta exitosa - Obtener opciones
```json
{
  "success": true,
  "data": [
    {
      "value": "VACACIONES",
      "label": "Vacaciones"
    },
    {
      "value": "MEDICO",
      "label": "Médico"
    },
    {
      "value": "ASUNTOS",
      "label": "Asuntos Propios"
    },
    {
      "value": "OTROS",
      "label": "Otros"
    }
  ]
}
```

---

## Script de prueba - Node.js

Guarda esto en un archivo `test-api.js`:

```javascript
const http = require('http');

const BASE_URL = 'http://localhost:8069';

function makeRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
        const url = new URL(path, BASE_URL);
        const options = {
            method: method,
            hostname: url.hostname,
            port: url.port,
            path: url.pathname + url.search,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        const req = http.request(options, (res) => {
            let responseData = '';
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseData));
                } catch (e) {
                    resolve(responseData);
                }
            });
        });

        req.on('error', reject);

        if (data) {
            req.write(JSON.stringify(data));
        }
        req.end();
    });
}

async function runTests() {
    console.log('🧪 Iniciando pruebas de API...\n');

    try {
        // Test 1: Obtener opciones
        console.log('📋 Test 1: Obtener opciones de tipo_motivo');
        const opciones = await makeRequest('GET', '/api/ausencias/opciones-tipo-motivo');
        console.log('✅ Respuesta:', JSON.stringify(opciones, null, 2));
        console.log('');

        // Test 2: Listar ausencias existentes
        console.log('📋 Test 2: Listar ausencias');
        const ausencias = await makeRequest('GET', '/api/ausencias/listar');
        console.log('✅ Respuesta:', JSON.stringify(ausencias, null, 2));
        console.log('');

        // Test 3: Crear una nueva ausencia
        console.log('📋 Test 3: Crear nueva ausencia');
        const nuevaAusencia = {
            fecha_inicio: '2024-06-15',
            fecha_fin: '2024-06-20',
            tipo_motivo: 'VACACIONES',
            descripcion_motivo: 'Prueba desde Node.js',
            hora_inicio: 8.0,
            hora_fin: 17.0,
            employee_id: 5
        };
        const resultado = await makeRequest('POST', '/api/ausencias/crear', nuevaAusencia);
        console.log('✅ Respuesta:', JSON.stringify(resultado, null, 2));
        console.log('');

        // Test 4: Listar nuevamente para confirmar
        console.log('📋 Test 4: Listar ausencias (después de crear)');
        const ausenciasActualizadas = await makeRequest('GET', '/api/ausencias/listar');
        console.log('✅ Total de ausencias:', ausenciasActualizadas.count);
        console.log('');

    } catch (error) {
        console.error('❌ Error:', error.message);
    }
}

runTests();
```

Ejecutar con:
```bash
node test-api.js
```

---

## Script de prueba - Python

Guarda esto en un archivo `test-api.py`:

```python
import requests
import json

BASE_URL = 'http://localhost:8069'

def test_api():
    print("🧪 Iniciando pruebas de API...\n")

    try:
        # Test 1: Obtener opciones
        print("📋 Test 1: Obtener opciones de tipo_motivo")
        response = requests.get(f'{BASE_URL}/api/ausencias/opciones-tipo-motivo')
        print(f"✅ Respuesta: {json.dumps(response.json(), indent=2)}\n")

        # Test 2: Listar ausencias
        print("📋 Test 2: Listar ausencias")
        response = requests.get(f'{BASE_URL}/api/ausencias/listar')
        data = response.json()
        print(f"✅ Respuesta: {json.dumps(data, indent=2)}\n")

        # Test 3: Crear ausencia
        print("📋 Test 3: Crear nueva ausencia")
        nueva_ausencia = {
            "fecha_inicio": "2024-06-25",
            "fecha_fin": "2024-06-28",
            "tipo_motivo": "VACACIONES",
            "descripcion_motivo": "Prueba desde Python",
            "hora_inicio": 8.0,
            "hora_fin": 17.0,
            "employee_id": 5
        }
        response = requests.post(
            f'{BASE_URL}/api/ausencias/crear',
            json=nueva_ausencia,
            headers={'Content-Type': 'application/json'}
        )
        print(f"✅ Respuesta: {json.dumps(response.json(), indent=2)}\n")

        # Test 4: Listar nuevamente
        print("📋 Test 4: Listar ausencias (después de crear)")
        response = requests.get(f'{BASE_URL}/api/ausencias/listar')
        data = response.json()
        print(f"✅ Total de ausencias: {data.get('count')}\n")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_api()
```

Ejecutar con:
```bash
pip install requests
python test-api.py
```

