# PROYECTO FINAL DE VENTAS 
## Instalación de Dependencias
```bash
pip install -r requirements.txt
```
## Configuración de PostgreSQL
1. Instalar PostgreSQL versión 14.
2. Durante la instalación, definir una contraseña para el usuario **postgres**.
3. Abrir una terminal y ejecutar:
   ```bash
   psql -U postgres
   ```
4. Ingresar la contraseña para acceder al Shell de PostgreSQL.
5. Crear la base de datos:
   ```sql
   CREATE DATABASE "e-commerce";
   ```
6. Salir del Shell de PostgreSQL.

## Configuración del Proyecto
1. En la raíz del proyecto, crear un archivo `.env` con la siguiente estructura:
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_DATABASE=e-commerce
   DB_USERNAME=postgres
   DB_PASSWORD=<Tu_Contraseña_Aquí>
   DB_SOCKET=localhost
   DB_PORT=5432
   ```
2. Ejecutar las migraciones:
   ```bash
   python manage.py migrate
   ```

## Configuración de Tailwind CSS
1. Navegar al directorio de Tailwind e iniciar el compilador:
   ```bash
   cd tailwind && npm run watch
   ```
2. Instalar plugins adicionales:
   ```bash
   npm install @tailwindcss/forms --save-dev
   npm install @tailwindcss/typography --save-dev
   npm install @tailwindcss/aspect-ratio --save-dev

## Levantar el servidor
    python manage.py runserver --nothreading

# Guía para Agregar Traducciones
## Pasos para agregar más palabras para la traducción
### 1. Agregar etiquetas de traducción en los archivos HTML
En los archivos HTML, agregamos la etiqueta `{% trans %}` a las palabras que queremos traducir.

Ejemplo:
- HTML antes:
  ```html
  ¡Bienvenido de vuelta!
  ```
- HTML con etiqueta:
  ```html
  {% trans '¡Bienvenido de vuelta!' %}
  ```
### 2. Agregar traducciones en el archivo de idioma
En la ruta `locate/en/LC_MESSAGES/django.po`, agregamos las nuevas traducciones.

Ejemplo:
```
msgid "¡Bienvenido de vuelta!"
msgstr "Welcome back!"
```
- `msgid`: Debe corresponder a un texto de los archivos HTML
- `msgstr`: Se coloca la traducción a inglés del texto

### 3. Compilar los mensajes
Abrimos una nueva terminal y ejecutamos el siguiente comando para guardar los cambios de la traducción:

```
django-admin compilemessages --verbosity=3
```

### 4. Recargar la página
Recargamos la página con `Ctrl + F5` o `Ctrl + Shift + R` (forzar recarga ignorando la caché).
