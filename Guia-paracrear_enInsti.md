# 🎯 Guía completa: Tu proyecto Doodba - Resumen de todo lo hecho

---

## ✅ Estado actual: TODO FUNCIONANDO

- **Odoo 17.0** corriendo en `http://localhost:17069`
- **PgWeb** (gestor de BD visual) en `http://localhost:17081`
- **MailHog** (email fake) en `http://localhost:17025`
- **Base de datos `devel`** inicializada con módulo `base`
- **Credenciales**: usuario `admin`, contraseña `admin` (por defecto de Odoo)

---

## OBJETIVO 1 — Lo que hicimos paso a paso

### Problema 1: Repositorio incorrecto
❌ `gh:Tecnativa/doodba` → Es la **imagen Docker**, NO la plantilla
✅ `gh:Tecnativa/doodba-copier-template` → Es la **plantilla de proyecto**

### Problema 2: Copier roto
- `copier 8.3.0` + `pyyaml-include v2` = módulo `yamlinclude` no encontrado
- La plantilla requiere `_min_copier_version: "9"`
- **Solución**: `pipx install copier` (instaló v9.11.3)

### Problema 3: Odoo no arrancaba (Exited 1)
- En modo `devel`, Odoo NO se descarga automáticamente
- Hay que ejecutar `setup-devel.yaml` para hacer **git-aggregate** (clonar OCB/Odoo)
- Luego hay que inicializar la BD con `-i base`

### Comandos exactos que ejecutamos (en orden):

```bash
# 1. Instalar copier correctamente
pipx uninstall copier
pipx install copier    # v9.11.3

# 2. Inicializar git en la carpeta del proyecto
cd ~/proyecto_odoo_adaptacion
git init

# 3. Generar el proyecto con copier
copier copy --trust --data-file /tmp/doodba-answers.yml --defaults \
  gh:Tecnativa/doodba-copier-template .

# 4. Construir la imagen Docker
docker compose -f docker-compose.yml build

# 5. Descargar código fuente de Odoo (git-aggregate)
export DOODBA_GITAGGREGATE_UID="$(id -u)"
export DOODBA_GITAGGREGATE_GID="$(id -g)"
export DOODBA_UMASK="$(umask)"
docker compose -f setup-devel.yaml run --rm odoo

# 6. Levantar todos los servicios
docker compose -f docker-compose.yml up -d

# 7. Inicializar la base de datos
docker compose -f docker-compose.yml run --rm \
  -l traefik.enable=false odoo \
  odoo -i base --stop-after-init -d devel

# 8. Reiniciar Odoo para que conecte con la BD
docker compose -f docker-compose.yml restart odoo
```

---

## 📁 Estructura del proyecto

```
proyecto_odoo_adaptacion/
├── .copier-answers.yml          ← Config guardada de copier
├── .docker/                     ← Contraseñas (NO va a git)
│   ├── db-access.env            ← Password BD para Odoo
│   ├── db-creation.env          ← Password BD para crear BD
│   └── odoo.env                 ← Admin password de Odoo
├── .gitignore                   ← Ya bien configurado
├── common.yaml                  ← Servicios Docker compartidos
├── devel.yaml                   ← Config de desarrollo
├── docker-compose.yml           ← = devel.yaml (symlink/copia)
├── prod.yaml                    ← Config de producción
├── setup-devel.yaml             ← Para hacer git-aggregate
├── test.yaml                    ← Config de testing
├── tasks.py                     ← Tareas invoke
├── odoo/
│   ├── Dockerfile               ← Imagen base doodba + personalización
│   ├── .dockerignore
│   ├── auto/                    ← Generado automáticamente (NO tocar)
│   │   ├── addons/              ← Symlinks a addons
│   │   └── odoo.conf            ← Config generada
│   └── custom/
│       ├── build.d/             ← Scripts extra al construir imagen
│       ├── conf.d/              ← Config extra de Odoo
│       ├── dependencies/        ← Dependencias del sistema
│       │   ├── apt.txt          ← Paquetes apt
│       │   ├── pip.txt          ← Paquetes Python
│       │   ├── npm.txt          ← Paquetes npm
│       │   └── gem.txt          ← Paquetes Ruby
│       ├── entrypoint.d/        ← Scripts al arrancar contenedor
│       ├── ssh/                 ← Claves SSH para repos privados
│       └── src/
│           ├── addons.yaml      ← Qué addons activar
│           ├── repos.yaml       ← Qué repos clonar
│           ├── odoo/            ← Código fuente Odoo (NO va a git)
│           └── private/         ← 🔥 TUS MÓDULOS VAN AQUÍ 🔥
│               └── .editorconfig
```

---

## 🔥 Dónde poner tus módulos personalizados

**Ruta exacta:**
```
/home/endika/proyecto_odoo_adaptacion/odoo/custom/src/private/
```

### Crear un módulo que hereda de otro (ejemplo: heredar `sale`):

```bash
mkdir -p odoo/custom/src/private/mi_modulo_venta/{models,views,security}
```

**Archivos necesarios:**

```python
# odoo/custom/src/private/mi_modulo_venta/__init__.py
from . import models
```

```python
# odoo/custom/src/private/mi_modulo_venta/models/__init__.py
from . import sale_order
```

```python
# odoo/custom/src/private/mi_modulo_venta/models/sale_order.py
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    campo_practica = fields.Char(string='Campo de práctica')
```

```python
# odoo/custom/src/private/mi_modulo_venta/__manifest__.py
{
    'name': 'Mi Módulo de Venta - Práctica',
    'version': '17.0.1.0.0',
    'author': 'Endika',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        # 'views/sale_order_view.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
}
```

**Después de crear el módulo:**
```bash
# Reiniciar Odoo
docker compose -f docker-compose.yml restart odoo

# Instalar el módulo (primera vez)
docker compose -f docker-compose.yml run --rm \
  -l traefik.enable=false odoo \
  odoo -i mi_modulo_venta --stop-after-init -d devel

# O actualizar si ya estaba instalado
docker compose -f docker-compose.yml run --rm \
  -l traefik.enable=false odoo \
  odoo -u mi_modulo_venta --stop-after-init -d devel

# Reiniciar para que el servidor vuelva al modo normal
docker compose -f docker-compose.yml restart odoo
```

---

## 🖥️ URLs útiles

| Servicio | URL | Para qué |
|---|---|---|
| **Odoo** | http://localhost:17069 | Aplicación principal |
| **PgWeb** | http://localhost:17081 | Ver/consultar la BD |
| **MailHog** | http://localhost:17025 | Emails enviados (fake) |
| **WDB** | http://localhost:17984 | Debugger Python web |

> 💡 El prefijo `17` viene del `PORT_PREFIX` que doodba calcula de la versión de Odoo.

---

## 🔄 Comandos del día a día

```bash
# Siempre desde ~/proyecto_odoo_adaptacion

# Levantar todo
docker compose -f docker-compose.yml up -d

# Parar todo
docker compose -f docker-compose.yml down

# Ver logs de Odoo en tiempo real
docker compose -f docker-compose.yml logs -f odoo

# Reiniciar solo Odoo (tras cambio en Python)
docker compose -f docker-compose.yml restart odoo

# Entrar al contenedor Odoo con bash
docker compose -f docker-compose.yml exec odoo bash

# Ver estado
docker compose -f docker-compose.yml ps
```

---

## OBJETIVO 2 — Transportar el proyecto al instituto

### Estrategia recomendada: **GitHub + imágenes Docker exportadas**

### Paso 1: Qué va a GitHub (código)

El `.gitignore` ya está bien configurado. Solo se subirá:

| ✅ SÍ sube a git | ❌ NO sube a git |
|---|---|
| `common.yaml`, `devel.yaml`, `prod.yaml` | `.docker/` (contraseñas) |
| `setup-devel.yaml`, `test.yaml` | `odoo/auto/` (generado) |
| `tasks.py` | `odoo/custom/src/odoo/` (38k archivos) |
| `odoo/Dockerfile` | `docker-compose.yml` (se regenera) |
| `odoo/custom/src/private/**` (tus módulos) | Volúmenes Docker |
| `odoo/custom/src/repos.yaml` | `.idea/` |
| `odoo/custom/src/addons.yaml` | |
| `odoo/custom/dependencies/*.txt` | |
| `.copier-answers.yml` | |

### Paso 2: Subir a GitHub

```bash
cd ~/proyecto_odoo_adaptacion

# Crear el archivo de contraseñas de ejemplo
mkdir -p .docker
echo "ADMIN_PASSWORD=cambiar-en-cada-entorno" > .docker/odoo.env.example
echo "PGPASSWORD=cambiar-en-cada-entorno" > .docker/db-access.env.example
echo "POSTGRES_PASSWORD=cambiar-en-cada-entorno" > .docker/db-creation.env.example

# Hacer el commit inicial
git add .
git status   # Revisar que NO sube cosas innecesarias
git commit -m "Proyecto doodba Odoo 17 - práctica adaptación"

# Conectar con GitHub (sustituye tu usuario real)
git remote add origin git@github.com:TU_USUARIO/proyecto-odoo-adaptacion.git
git branch -M main
git push -u origin main
```

### Paso 3: Exportar imágenes Docker (para offline)

```bash
# Ver las imágenes que usa tu proyecto
docker compose -f docker-compose.yml config --images > /tmp/images_list.txt
cat /tmp/images_list.txt

# Exportar TODAS las imágenes necesarias
docker save \
  proyecto_odoo_adaptacion-odoo:latest \
  ghcr.io/tecnativa/postgres-autoconf:17-alpine \
  ghcr.io/tecnativa/docker-whitelist:latest \
  docker.io/mailhog/mailhog \
  docker.io/kozea/wdb \
  docker.io/sosedoff/pgweb \
  | gzip > ~/odoo-imagenes-instituto.tar.gz

# Verificar tamaño
ls -lh ~/odoo-imagenes-instituto.tar.gz
```

> ⚠️ Esto puede pesar 2-4 GB. Llévalo en USB.

### Paso 4: En el instituto (offline)

```bash
# 1. Clonar el repositorio (si hay internet ese momento)
git clone git@github.com:TU_USUARIO/proyecto-odoo-adaptacion.git
cd proyecto-odoo-adaptacion

# O si no hay internet, copia la carpeta del USB directamente

# 2. Cargar las imágenes Docker desde USB
docker load < /ruta/usb/odoo-imagenes-instituto.tar.gz

# 3. Crear los archivos de contraseñas
mkdir -p .docker
echo "ADMIN_PASSWORD=admin-password-practica" > .docker/odoo.env
echo "PGPASSWORD=odoo-db-password" > .docker/db-access.env
echo "POSTGRES_PASSWORD=odoo-db-password" > .docker/db-creation.env

# 4. Crear el docker-compose.yml (el gitignore lo excluye)
cp devel.yaml docker-compose.yml

# 5. Descargar código fuente de Odoo (necesita internet O copiarlo del USB)
export DOODBA_GITAGGREGATE_UID="$(id -u)"
export DOODBA_GITAGGREGATE_GID="$(id -g)"
export DOODBA_UMASK="$(umask)"
docker compose -f setup-devel.yaml run --rm odoo

# 6. Levantar servicios
docker compose -f docker-compose.yml up -d

# 7. Inicializar BD
docker compose -f docker-compose.yml run --rm \
  -l traefik.enable=false odoo \
  odoo -i base --stop-after-init -d devel

# 8. Reiniciar
docker compose -f docker-compose.yml restart odoo
```

### Paso 5 (alternativa TOTALMENTE offline): Copiar también `odoo/custom/src/odoo/`

Si en el instituto **NO hay internet para nada**, también necesitas el código fuente de Odoo:

```bash
# En casa: comprimir el código fuente
tar czf ~/odoo-src-17.tar.gz -C ~/proyecto_odoo_adaptacion/odoo/custom/src odoo

# En instituto: descomprimir
tar xzf /ruta/usb/odoo-src-17.tar.gz -C ~/proyecto-odoo-adaptacion/odoo/custom/src/
```

---

## ⚡ Flujo de trabajo diario

```
CASA                                    INSTITUTO
────                                    ─────────
1. Editar módulo en                     5. git pull (si hay internet)
   odoo/custom/src/private/                o copiar desde USB

2. Probar en localhost:17069            6. docker compose up -d

3. git add + commit + push              7. Instalar/actualizar módulo

4. Si cambió Dockerfile:               8. Probar / Presentar
   exportar imagen de nuevo
```

---

## ⚠️ Errores comunes y soluciones

| Error | Causa | Solución |
|---|---|---|
| `Exited (1)` en contenedor odoo | Código fuente no descargado | Ejecutar `setup-devel.yaml` |
| `Database not initialized` | BD vacía | Ejecutar `-i base --stop-after-init` |
| Puerto `17069` ocupado | Otro proyecto doodba | Cambiar `PORT_PREFIX` en `.env` o exportar la variable |
| Módulo no aparece | No reiniciaste Odoo | `docker compose restart odoo` |
| Permiso denegado en `src/` | UID diferente | `sudo chown -R $(id -u):$(id -g) odoo/` |
| `version is obsolete` | Warning de compose v2 | **Ignorar**, no es un error, es un aviso |
| Copier falla con `yamlinclude` | `pyyaml-include` v2 incompatible | Reinstalar copier con `pipx` |
| `No git tags found` | Repo incorrecto (doodba vs template) | Usar `gh:Tecnativa/doodba-copier-template` |
