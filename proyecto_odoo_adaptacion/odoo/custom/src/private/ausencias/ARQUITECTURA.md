# 📊 Arquitectura de la API de Ausencias

## Diagrama General

```
┌─────────────────────┐
│   Aplicación React  │
│   (Frontend)        │
└──────────┬──────────┘
           │
           │ HTTP(S)
           │ Fetch/Axios
           │
           ▼
┌─────────────────────────────────────────┐
│        Odoo 17 (localhost:8069)         │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Módulo: ausencias                │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │   Controllers (API)         │ │ │
│  │  │                             │ │ │
│  │  │  GET  /api/ausencias/listar │ │ │
│  │  │  POST /api/ausencias/crear  │ │ │
│  │  │  GET  /api/ausencias/...    │ │ │
│  │  └────────────┬────────────────┘ │ │
│  │               │                  │ │
│  │  ┌────────────▼──────────────┐  │ │
│  │  │   Models                  │  │ │
│  │  │                           │  │ │
│  │  │  ausencias.solicitudes    │  │ │
│  │  │   - employee_id           │  │ │
│  │  │   - fecha_inicio          │  │ │
│  │  │   - fecha_fin             │  │ │
│  │  │   - tipo_motivo           │  │ │
│  │  │   - descripcion_motivo    │  │ │
│  │  └────────────┬──────────────┘  │ │
│  │               │                  │ │
│  │  ┌────────────▼──────────────┐  │ │
│  │  │   PostgreSQL Database     │  │ │
│  │  │   (Tabla: ausencias_      │  │ │
│  │  │    solicitudes)           │  │ │
│  │  └───────────────────────────┘  │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
           ▲
           │ PyODOO / REST API
           │ (Interno)
           │
       ┌───┴──────────────┐
       │  Modelos Odoo    │
       │  - hr.employee   │
       │  - res.users     │
       └──────────────────┘
```

---

## Flujo de Solicitud

### 1. Obtener Lista de Ausencias

```
React Client
    │
    ├─> GET /api/ausencias/listar
    │
    └─> HTTP Response with JSON
        {
            "success": true,
            "data": [...],
            "count": n
        }
```

### 2. Crear Nueva Ausencia

```
React Client
    │
    ├─> POST /api/ausencias/crear
    │   Body: {
    │       fecha_inicio: "2024-05-15",
    │       fecha_fin: "2024-05-17",
    │       tipo_motivo: "VACACIONES",
    │       descripcion_motivo: "..."
    │   }
    │
    ├─> Validate Data
    │
    ├─> Create Record in DB
    │
    └─> HTTP Response with JSON
        {
            "success": true,
            "ausencia": {...}
        }
```

---

## Estructura de Archivos

```
ausencias/
├── 📄 README.md                    # Resumen general
├── 📄 INICIO_RAPIDO.md            # Guía 5 minutos
├── 📄 API_DOCUMENTATION.md        # Docs completas
├── 📄 EJEMPLOS_SOLICITUDES.md     # Ejemplos cURL, Postman, Python
├── 📄 SEGURIDAD_CONFIGURACION.md  # Seguridad y CORS
├── 🐍 client_ausencias_api.py     # Cliente Python ejecutable
│
├── controllers/
│   ├── __init__.py
│   └── controllers.py             # ✏️ MODIFICADO - Endpoints API
│
├── models/
│   └── ausencia.py                # Modelo de datos (sin cambios)
│
├── views/
│   └── views.xml                  # Vistas Odoo
│
├── security/
│   └── ir.model.access.csv        # Permisos
│
├── demo/
│   └── demo.xml
│
├── report/
│
├── static/
│
├── __manifest__.py                 # Configuración del módulo
└── __init__.py
```

---

## Flujo de Desarrollo

```
1. Tu Aplicación React
   └─> Necesita conectar con Odoo ausencias

2. He creado 3 Endpoints REST
   ├─> GET  /api/ausencias/listar
   ├─> POST /api/ausencias/crear
   └─> GET  /api/ausencias/opciones-tipo-motivo

3. Archivos Generados
   ├─> controllers.py (lógica API)
   ├─> client_ausencias_api.py (cliente Python)
   └─> Documentación completa

4. Tu puedes ahora
   ├─> Hacer fetch desde React
   ├─> Integrar con formularios
   ├─> Mostrar datos en tablas
   └─> Enviar datos a Odoo

5. Los datos se guardan
   └─> En la DB de Odoo
       └─> Modelo: ausencias.solicitudes
           └─> Visible en Odoo Web
```

---

## Endpoints REST

```
┌─────────────────────────────────────────────────────┐
│ Endpoint 1: Listar Ausencias                        │
├─────────────────────────────────────────────────────┤
│ Método: GET                                         │
│ URL: /api/ausencias/listar                          │
│ Auth: public                                        │
│ CSRF: deshabilitado                                 │
│ Retorna: JSON con lista de ausencias                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Endpoint 2: Crear Ausencia                          │
├─────────────────────────────────────────────────────┤
│ Método: POST                                        │
│ URL: /api/ausencias/crear                           │
│ Auth: public                                        │
│ CSRF: deshabilitado                                 │
│ Recibe: JSON con datos de ausencia                  │
│ Retorna: JSON con ausencia creada                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Endpoint 3: Opciones Tipo Motivo                    │
├─────────────────────────────────────────────────────┤
│ Método: GET                                         │
│ URL: /api/ausencias/opciones-tipo-motivo            │
│ Auth: public                                        │
│ CSRF: deshabilitado                                 │
│ Retorna: JSON con opciones para Select              │
└─────────────────────────────────────────────────────┘
```

---

## Esquema de Datos

```
┌─────────────────────────────────────────────┐
│  Model: ausencias.solicitudes               │
├─────────────────────────────────────────────┤
│ ID (PK)                    INTEGER          │
│ employee_id (FK)           MANY2ONE → hr.e  │
│ fecha_inicio              DATE              │
│ hora_inicio               FLOAT             │
│ fecha_fin                 DATE              │
│ hora_fin                  FLOAT             │
│ tipo_motivo               SELECTION         │
│ descripcion_motivo        TEXT              │
│ created_at                TIMESTAMP         │
│ updated_at                TIMESTAMP         │
└─────────────────────────────────────────────┘
```

---

## Ciclo de Vida de una Solicitud

```
1. CLIENT (React)
   └─> Click en "Crear Ausencia"

2. JS EVENT HANDLER
   └─> Recolecta datos del formulario

3. FETCH REQUEST
   └─> Envía POST a /api/ausencias/crear

4. HTTP TRANSPORT
   └─> Internet → localhost:8069

5. SERVER (Odoo)
   └─> Request llega a Odoo

6. ROUTING
   └─> @http.route() mapea a método

7. VALIDATION
   └─> Valida tipos y campos requeridos

8. DATABASE
   └─> CREATE: INSERT INTO ausencias_solicitudes

9. RESPONSE GENERATION
   └─> {"success": true, "ausencia": {...}}

10. HTTP TRANSPORT
    └─> Response → Cliente

11. CLIENT (React)
    └─> .json() parse
    └─> State update
    └─> UI refresh
```

---

## Seguridad - Niveles

```
Nivel 1: ACTUAL (Desarrollo)
├─> auth='public'
├─> csrf=False
├─> Sin autenticación
└─> ✅ Para desarrollo local

Nivel 2: RECOMENDADO (Testing)
├─> auth='user'
├─> csrf=True (default)
├─> Require login
└─> ✅ Para testing

Nivel 3: SEGURO (Producción)
├─> Autenticación JWT
├─> Rate limiting
├─> HTTPS obligatorio
├─> Logging completo
└─> ✅ Para producción
```

---

## Herramientas y Dependencias

| Herramienta | Propósito | Incluido |
|-----------|-----------|----------|
| Odoo 17 | Framework | ✅ Ya existe |
| Python | Backend | ✅ Ya existe |
| HTTP | Protocolo | ✅ Nativo Odoo |
| JSON | Formato datos | ✅ Nativo Python |
| PostgreSQL | Database | ✅ Ya existe |
| React | Frontend | 📦 En tu proyecto |

---

## Flujo de Integración con React

```
Tu App React
    │
    ├─> import { AusenciasForm } from './components'
    │
    ├─> <AusenciasForm />
    │
    └─> Dentro del componente:
        │
        ├─> useState() - gestionar formulario
        ├─> useEffect() - cargar opciones
        ├─> fetch() - llamar API
        │
        └─> Render:
            ├─> Inputs
            ├─> Select (con opciones del server)
            ├─> Button
            └─> Feedback al usuario
                ├─> Éxito: "Creada con ID #"
                └─> Error: "No se pudo crear"
```

---

## Testing

```
cURL
├─> curl http://localhost:8069/api/ausencias/listar
└─> curl -X POST ... -d '{...}'

Postman
├─> Importar colección
├─> Configurar variables
└─> Ejecutar requests

Python
├─> pip install requests
├─> run test-api.py
└─> Ver resultados

Node.js
├─> node test-api.js
└─> Ver resultados

React
├─> fetch() en componentes
├─> Mostrar en UI
└─> Verificar en Odoo
```

---

## Status General

```
✅ Endpoints creados        - Listos para usar
✅ Validaciones              - Implementadas
✅ Manejo de errores         - JSON responses
✅ Documentación             - Completa
✅ Ejemplos de código        - 5+ lenguajes
✅ Cliente Python            - Ejecutable
✅ Sin cambios al modelo     - Compatible
✅ API Testing               - Scripts incluidos

⚠️  CORS                     - Necesita config
⚠️  Autenticación            - Actualmente public
⚠️  Rate Limiting            - No implementado
⚠️  HTTPS                    - Para producción
⚠️  Logging avanzado         - Opcional

🔜 Recomendaciones futuras:
   - Implementar auth tokens
   - Agregar rate limiting
   - Configurar CORS
   - Agregar más validaciones
   - Implementar pagginación
```

---

**Diagrama creado: Sistema completamente funcional** ✨

