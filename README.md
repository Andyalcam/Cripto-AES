# Examen primera parte. Expansion de llaves

Alvarado Camacho Andrea		318064343
---

## Instrucciones para Ejecutar el Proyecto con Docker

A continuación se describen los pasos para ejecutar el proyecto de expansión de llaves AES en Docker:

### 1. Clonar el Repositorio

Primero, clona el repositorio en tu máquina local usando el siguiente comando:

```bash
git clone https://gitlab.com/Andyalcam/Cripto-AES.git
```
Luego colocate a la altura de el archivo ```expansionLlaves.py``` con el comando:
```bash
cd Cripto-AES
```

### 2. Crear la imagen

Debes crear una imagen cambiando el nombre de la etiqueta por ejemplo:

```bash
docker build -t aes-expansion-llaves .
```
y verifica que exista con:

```bash
docker image ls
```

### 3. Ejecutar el contenedor

Una vez que se haya creado la imagen con exito puedes correr el contenedor con el siguiente codigo:

```bash
docker run aes-expansion-llaves
``