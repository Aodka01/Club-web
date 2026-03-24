# Clubes ITSC

## Descripción

Proyecto Django para la gestión de clubes estudiantiles del ITSC.
Incluye control de usuarios, roles (Coordinador/Estudiante), clubes, eventos, comentarios, inscripciones de eventos y modo oscuro.

## Características

- Autenticación de usuario (login/logout/password reset)
- Perfil de usuario con avatar, bio y datos de carrera/semestre o área de maestro
- Roles y permisos con grupos de Django: `Coordinador`, `Estudiante`
- Creación/edición/eliminación de clubes (coordinador/creador)
- Creación/edición/eliminación de eventos
- Inscripción a eventos con control de cupo y listado de asistentes
- Comentarios en eventos con opciones de eliminación por autor o coordinador
- UI con tema rojo y opción de `dark mode` persistente

## Modelo de datos

- `User` (Django)
- `Profile` (OneToOne con User)
- `Club` (nombre, descripción, categoría, color, imagen, creador)
- `Membership` (usuario-club)
- `Event` (número de cupo, fecha/hora, lugar, creador)
- `EventComment` (event-comentario)
- `EventAttendance` (inscripción a evento)

## Instrucciones de instalación

1. Clonar el repositorio
2. Crear y activar entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Migrar base de datos:

```bash
python manage.py migrate
```

5. Crear superusuario:

```bash
python manage.py createsuperuser
```

6. Ejecutar servidor:

```bash
python manage.py runserver
```

7. Abrir en `http://127.0.0.1:8000/`

## Uso

- `Coordinador`: crea/edita/elimina clubes y eventos; administra miembros.
- `Estudiante`: se une a clubes, participa en eventos, comenta.

## Notas

- Las imágenes se almacenan en `media/`.
- Asegurarse de tener `MEDIA_URL` y `MEDIA_ROOT` configurados en `settings.py`.

## Mejoras futuras

- Pagos / checkout para eventos premium
- Notificaciones por email
- Chat en vivo para eventos

## aodka
