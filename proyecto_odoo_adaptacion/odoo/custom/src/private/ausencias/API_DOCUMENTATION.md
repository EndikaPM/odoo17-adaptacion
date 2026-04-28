# API de Ausencias - Documentación

## Descripción
Esta API permite que aplicaciones externas (como React) interactúen con el módulo de ausencias en Odoo.

---

## Endpoints Disponibles

### 1. **Listar todas las ausencias**

**Método:** `GET`
**URL:** `/api/ausencias/listar`
**Autenticación:** No requerida (public)

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "employee_id": 5,
            "employee_name": "Juan Pérez",
            "fecha_inicio": "2024-04-27",
            "hora_inicio": 9.0,
            "fecha_fin": "2024-05-01",
            "hora_fin": 17.0,
            "tipo_motivo": "VACACIONES",
            "descripcion_motivo": "Vacaciones de primavera"
        }
    ],
    "count": 1
}
```

**Respuesta con error (500):**
```json
{
    "success": false,
    "error": "Descripción del error"
}
```

**Ejemplo en React:**
```javascript
fetch('http://localhost:8069/api/ausencias/listar')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Ausencias:', data.data);
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => console.error('Error de conexión:', error));
```

---

### 2. **Crear una nueva ausencia**

**Método:** `POST`
**URL:** `/api/ausencias/crear`
**Autenticación:** No requerida (public)
**Content-Type:** `application/json`

**Body requerido:**
```json
{
    "employee_id": 5,  (opcional - si no viene se infiere del usuario)
    "fecha_inicio": "2024-04-27",  (requerido)
    "hora_inicio": 9.0,  (opcional)
    "fecha_fin": "2024-05-01",  (requerido)
    "hora_fin": 17.0,  (opcional)
    "tipo_motivo": "VACACIONES",  (requerido - ver opciones disponibles)
    "descripcion_motivo": "Descripción de la ausencia"  (requerido)
}
```

**Valores válidos para `tipo_motivo`:**
- `VACACIONES` - Vacaciones
- `MEDICO` - Médico
- `ASUNTOS` - Asuntos Propios
- `OTROS` - Otros

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Ausencia creada exitosamente",
    "ausencia": {
        "id": 2,
        "employee_id": 5,
        "employee_name": "Juan Pérez",
        "fecha_inicio": "2024-05-10",
        "hora_inicio": 8.0,
        "fecha_fin": "2024-05-12",
        "hora_fin": 17.0,
        "tipo_motivo": "MEDICO",
        "descripcion_motivo": "Cita médica con especialista"
    }
}
```

**Respuesta con error (200 - validación):**
```json
{
    "success": false,
    "error": "Descripción del error - campo requerido, valor inválido, etc."
}
```

**Ejemplo en React:**
```javascript
const nuevaAusencia = {
    fecha_inicio: "2024-05-15",
    fecha_fin: "2024-05-17",
    tipo_motivo: "ASUNTOS",
    descripcion_motivo: "Asuntos personales importantes",
    hora_inicio: 8.0,
    hora_fin: 17.0
};

fetch('http://localhost:8069/api/ausencias/crear', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(nuevaAusencia)
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Ausencia creada:', data.ausencia);
        alert(`Ausencia creada exitosamente. ID: ${data.ausencia.id}`);
    } else {
        console.error('Error:', data.error);
        alert(`Error: ${data.error}`);
    }
})
.catch(error => console.error('Error de conexión:', error));
```

---

### 3. **Obtener opciones de tipo_motivo**

**Método:** `GET`
**URL:** `/api/ausencias/opciones-tipo-motivo`
**Autenticación:** No requerida (public)

**Respuesta exitosa (200):**
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

**Ejemplo en React (para un Select):**
```javascript
import React, { useState, useEffect } from 'react';

function FormAusencia() {
    const [opciones, setOpciones] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8069/api/ausencias/opciones-tipo-motivo')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    setOpciones(data.data);
                }
            })
            .catch(error => console.error('Error:', error));
    }, []);

    return (
        <select>
            {opciones.map(opcion => (
                <option key={opcion.value} value={opcion.value}>
                    {opcion.label}
                </option>
            ))}
        </select>
    );
}

export default FormAusencia;
```

---

## Notas Importantes

1. **CORS**: Si la aplicación React está en un dominio diferente a Odoo, es posible que necesites configurar CORS en Odoo.

2. **Autenticación**: Los endpoints actuales son públicos (`auth='public'`). Para mayor seguridad, considera cambiar a `auth='user'` o implementar autenticación.

3. **Fechas**: Las fechas deben estar en formato `YYYY-MM-DD` (ISO 8601).

4. **Horas**: Las horas están en formato decimal (9.0 = 9:00 AM, 14.5 = 14:30).

5. **Employee ID**: Si no se proporciona `employee_id`, se intentará obtener del usuario autenticado. Si tampoco está disponible de esa forma, la API retornará un error.

---

## Ejemplo de Aplicación React Completa

```javascript
import React, { useState, useEffect } from 'react';

function AusenciasApp() {
    const [ausencias, setAusencias] = useState([]);
    const [opciones, setOpciones] = useState([]);
    const [formData, setFormData] = useState({
        fecha_inicio: '',
        fecha_fin: '',
        tipo_motivo: 'VACACIONES',
        descripcion_motivo: '',
        hora_inicio: 9,
        hora_fin: 17
    });

    // Cargar ausencias y opciones al montar
    useEffect(() => {
        cargarAusencias();
        cargarOpciones();
    }, []);

    const cargarAusencias = async () => {
        try {
            const response = await fetch('http://localhost:8069/api/ausencias/listar');
            const data = await response.json();
            if (data.success) {
                setAusencias(data.data);
            }
        } catch (error) {
            console.error('Error al cargar ausencias:', error);
        }
    };

    const cargarOpciones = async () => {
        try {
            const response = await fetch('http://localhost:8069/api/ausencias/opciones-tipo-motivo');
            const data = await response.json();
            if (data.success) {
                setOpciones(data.data);
            }
        } catch (error) {
            console.error('Error al cargar opciones:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8069/api/ausencias/crear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            const data = await response.json();
            if (data.success) {
                alert('Ausencia creada exitosamente');
                cargarAusencias();
                // Resetear formulario
                setFormData({
                    fecha_inicio: '',
                    fecha_fin: '',
                    tipo_motivo: 'VACACIONES',
                    descripcion_motivo: '',
                    hora_inicio: 9,
                    hora_fin: 17
                });
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Error al crear ausencia:', error);
            alert('Error al conectar con el servidor');
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <div className="ausencias-app">
            <div className="form-section">
                <h2>Crear Nueva Ausencia</h2>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>Fecha de Inicio:</label>
                        <input
                            type="date"
                            name="fecha_inicio"
                            value={formData.fecha_inicio}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div>
                        <label>Fecha de Fin:</label>
                        <input
                            type="date"
                            name="fecha_fin"
                            value={formData.fecha_fin}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div>
                        <label>Tipo de Motivo:</label>
                        <select
                            name="tipo_motivo"
                            value={formData.tipo_motivo}
                            onChange={handleChange}
                        >
                            {opciones.map(opt => (
                                <option key={opt.value} value={opt.value}>
                                    {opt.label}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label>Descripción:</label>
                        <textarea
                            name="descripcion_motivo"
                            value={formData.descripcion_motivo}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <button type="submit">Crear Ausencia</button>
                </form>
            </div>

            <div className="list-section">
                <h2>Ausencias Registradas</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Empleado</th>
                            <th>Inicio</th>
                            <th>Fin</th>
                            <th>Tipo</th>
                            <th>Descripción</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ausencias.map(ausencia => (
                            <tr key={ausencia.id}>
                                <td>{ausencia.employee_name}</td>
                                <td>{ausencia.fecha_inicio}</td>
                                <td>{ausencia.fecha_fin}</td>
                                <td>{ausencia.tipo_motivo}</td>
                                <td>{ausencia.descripcion_motivo}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AusenciasApp;
```

---

## Solución de Problemas

### Error: "CORS policy"
Si obtienes errores de CORS, necesitas configurar CORS en Odoo. Contacta al administrador del servidor.

### Error: "employee_id no encontrado"
Asegúrate de proporcionar un `employee_id` válido o de estar autenticado como un usuario con empleado asociado.

### Error: "tipo_motivo inválido"
Verifica que `tipo_motivo` sea uno de los valores válidos: `VACACIONES`, `MEDICO`, `ASUNTOS`, `OTROS`.

### Error: "Conexión rechazada"
Verifica que:
- El servidor Odoo esté corriendo en `localhost:8069` (o el puerto/dominio correcto)
- La URL de la API sea correcta
- El navegador tenga acceso al servidor

