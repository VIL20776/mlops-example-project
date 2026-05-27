# Proyecto de ejemplo de uso de la infraestructura MLOps

Este repositorio sirve como una referencia para futuros proyectos que hagan uso de la infraestructura 
basada en Machine Learning Operations (MLOps) desarrollda para la Universidad del Valle de Guatemala.

## Componentes de un proyecto
Dado que los proyectos pueden tener necesidades diferentes, no fuerza una estructura estricta. Sin embargo, 
se espera que existan los siguientes componentes para poder hacer uso de la infraestructura:

* **Código del modelo (core.py):** Codigo fuente del modelo y otras utilidades necesarias para su construcción. 
Recuerda incluir estos archivos al Dockerfile.
* **Código de entrenamiento/experimentación (train.py)**: 
Código fuente definiendo la configuración, parametrización y datos a usar para el entrenamiento del modelo 
desarrollado. Puede definir multiples configuraciones para realizar pruebas y usar multiples archivos, pero 
recurda agregarlo todo al Dockerfile y definir un punto de entrada.
Más información en la sección de [Integración con MLFlow](./docs/MLFLOW.md).
Nota: Usa la API de boto3 para descargar los archivos necesarios, como se muestra en el programa de ejemplo.
* **Script/Programa de carga de datos (loader.py):**
Define los datos de entrenamiento a usar la bucket de datos de la infraestructura. Puede ser un script 
independiente, pero es recomendable integrarlo al código de entrenamiento. Usa la variable de entorno `DATA_BUCKET_NAME` 
para referirte a la bucket dentro del script/programa.<br>
Toma en cuenta que las maquinas virtuales usadas para el entrenamiento de los modelos no tienen acceso a 
internet. Por lo que si necesitas de un dataset particular que no se encuentre disponible en la infraestructura. 
Deberás solicitar al aministrador o a un operador que lo agreguen.
* **Dockerfile**: 
Define la imagen de entrenamiento que será usada para realizar el entrenamiento del modelo. Dentro debes definir 
el entorno de ejecución, las dependencias, los archivos necesarios para construir el modelo y otras configuraciones 
necesarias. Al final del Dockerfile agrega un comando `CMD` o `ENTRYPOINT` para definir el ejecutable para iniciar 
el entrenamiento.
NOTA: Si el cargador de datos es un programa/script independiente del código de entrenamiento, debes agregar un 
paso que ejecute el programa/script.
* **Script/Programa de descarga del modelo (deploy/download_model.py):** 
Define la descarga del modelo desde el registro de MLFlow. De ser necesario, modifique el script y el archivo 
requirements.txt para que pueda descargar el modelo correctamente.
Vea la sección de [Github Actions](#github-actions).

