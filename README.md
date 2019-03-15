# ChangePop
Repositorio destinado a la asignatura Proyecto Software 2019 UNIZAR: portal de compra/venta e intercambio de productos de segunda mano, con funcionalidades varias interesantes para los compradores y vendedores de productos

## Instalación

### Descargar
- Python 3.7.2 https://www.python.org/downloads/
  - Instalar pip tambien (viene por defecto)
- Flask $> ```pip install flask```
- Virtual Envs:
  - $> ```pip install virtualenv```
  - $> ```pip install virtualenvwrapper-win```
- PyCharm (recomendado): https://www.jetbrains.com/pycharm/

### Modo sin PyCharm
1) Clonar repositorio
2) Abrir cmd/powershell en el direcotrio del repositorio
3) Ejecutar los siguientes comandos:
  - $> ```mkvirtualenv venv```
  - $> ```workon venv```
  - $> ```setprojectdir .```
  - $> ```pip install .```
  - $> ```set FLASK_DEBUG=true```
  - $> ```set FLASK_APP=ChangePop```
  - $> ```set FLASK_ENV=development```
4) para acabar $> ```flask run```
7) Ya tienes el servidor funcionando en http://127.0.0.1:5000/

### Modo con PyCharm
1) Clonar Repositorio
2) Abrir la carpeta del repositorio con PyCharm (File > Open...)
3) En el terminal de pycharm (la de python no) escribir ```pip install .```
4) Ir a Run > Edit Configuration...
5) Añadir (+) > Flask, Comletar con la siguiente Configuración
  - Target Type: Module Name
  - Target: "ChangePop"
  - FLASK_ENV: "development"
  - FLASK_DEBUG: check
  - Environment
    - Environment variables: Añadir:
      - Name: FLASK_APP - Value: ChangePop
    - Python interpreter: Python 3.7
6) Run > Run(Flask 'ChangePop')
7) Ya tienes el servidor funcionando en http://127.0.0.1:5000/
