# Archivo principal de código Python para iniciar la aplicación

# Importando desde el paquete de la página web
from website import create_webapp

# Generando la aplicación
app = create_webapp()

app.config['TIMEOUT'] = 60

# Si se ejecuta directamente el main, se inicia el servidor web.
if __name__ == "__main__":

    # Si debug es True, el servidor se reiniciará automáticamente para reflejar los cambios en el código.
    app.run(debug=True) # El debug se establecerá en False una vez que la producción haya finalizado.
