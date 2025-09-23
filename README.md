# RynEditor

RynEditor es un editor de novelas visuales compatible con Ren'Py.

## Características

- Editor visual para crear novelas interactivas
- Compatible con el motor de Ren'Py
- Interfaz moderna y fácil de usar
- Soporte para múltiples plataformas

## Demo

Puedes ver la aplicación en funcionamiento visitando: [https://ryneditor.github.io](https://ryneditor.github.io)

## Instalación Local

Si quieres ejecutar la aplicación localmente:

1. Clona el repositorio:
```bash
git clone https://github.com/ryneditor/ryneditor.github.io.git
cd ryneditor.github.io
```

2. Sirve los archivos estáticos usando cualquier servidor HTTP local:
```bash
# Con Python
python -m http.server 8000

# Con Node.js (si tienes http-server instalado)
npx http-server

# Con PHP
php -S localhost:8000
```

3. Abre tu navegador en `http://localhost:8000`

## Desarrollo

Este proyecto está construido con React y se despliega automáticamente a GitHub Pages cuando se hace push a la rama principal.

## Licencia

Este proyecto está bajo la Licencia MIT.
