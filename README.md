# CEMV | Centro de Eventos y Monitoreo Virtual 
### Desarrollado por Carlos Emilio Mejía Vázquez
### Supervizado por el Ing. Mario Daniel Pascual Elizalde

Este es un proyecto que va a servir de herramienta para el Area de Sistemas en la Universidad de Ecatepec para llevar un control y monitoreo de todos los eventos que ocurren dentro de la universidad y están relacionados con el area.

# Requisitos
El programa ocupa Python 3.12.0.

## Librerías

| Package | Version |
| --------- | ------- |
| altgraph                 | 0.17.4 |
| asttokens                | 2.4.1 |
| colorama                 | 0.4.6 |
| executing                | 2.0.1 |
| icecream                 | 2.1.3 |
| mariadb                  | 1.1.8 |
| packaging                | 23.2 |
| pefile                   | 2023.2.7 |
| pip                      | 23.3.1 |
| Pygments                 | 2.17.2 |
| pyinstaller              | 6.3.0 |
| pyinstaller-hooks-contrib | 2023.10 |
| pyperclip                | 1.8.2 |
| PySimpleGUI              | 4.60.5 |
| pywin32-ctypes           | 0.2.2 |
| setuptools               | 69.0.2 |
| six                      | 1.16.0 |

Ejecuta el siguiente código en la terminal para poder instalar las librerías:
> Descarga el archivo "req.txt".
```bash
python -m pip install -r req.txt 
```

## Crear un ejecutable

Para crear un ejecutable con `pyinstaller`:

> Debes de ejecutar el comando en la misma ruta que el proyecto

```bash
pyinstaller [archivo main_vX_X_XBX.py] -F -n "nombre_del_ejecutable.exe" -w -i "\ruta\al\icono\CEMV-5.ico"
```
