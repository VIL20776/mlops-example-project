# Proyecto de ejemplo de uso de la infraestructura MLOps

Este repositorio sirve como una referencia para futuros proyectos que hagan uso de la infraestructura 
basada en Machine Learning Operations (MLOps) desarrollda para la Universidad del Valle de Guatemala.

## Componentes de un proyecto
Los proyectos de hagan uso de la infraestructura deben contar con los siguientes componentes:

* **Código de entrenamiento (train.py, utils.py)**: 
Código fuente definiendo la configuración y definición del modelo desarrollado. Multiples archivos se pueden usar, pero recurda agregarlos todos al Dockerfile. Más información en la sección de [Integración con MLFlow](#integración-con-mlflow).
* **Script/Programa de carga de datos (loader.py):**
Define los datos de entrenamiento a usar la bucket de datos de la infraestructura. Usa la variable de entorno `DATA_BUCKET_NAME` para referirte a la bucket dentro del script/programa.<br>
Toma en cuenta que las maquinas virtuales usadas
para el entrenamiento de los modelos no tienen acceso a internet. Por lo que si necesitas de un dataset particular que no se encuentre disponible en la infraestructura. Deberás solicitar al aministrador o a un operador que lo agreguen.
* **Dockerfile**: 
Define la imagen de entrenamiento que será usada para realizar el entrenamiento del modelo.
Dentro debes definir el entorno de ejecución, las dependencias y los archivos necesarios para construir el
modelo. Si el cargador de datos es un programa/script independiente del código de entrenamiento, debes agregar un paso que ejecute el programa/script.
* **Script/Programa de descarga del modelo (deploy/download_model.py):** 
Define la descarga del modelo desde el registro de MLFlow. 
Este archivo no debería ser modificado. Vea la sección de [Github Actions](#github-actions).

## Github Actions
En el proyecto se definen 3 workflows para el proceso de CI/CD.

+ **build-taining.yml:** Se encarga de construir la imagen de entrenamiento y subirla a la infraestructura.
+ **train.yml:** Se encarga de invocar crear la maquina virtual donde se entrenará el modelo.
+ **deploy.yml:** Se encarga de subir el modelo aprobado al registro de modelos.

Para el correcto funcionamiento de los workflows, es necesario definir los siguientes secretos en el repositorio del proyecto:

+ **PROJECT_ID:** Identificación del projecto dentro de la infraestructura. Lleva la estructura de 
{Usuario/Organización}-{LibreríaML}-{NombreDelRepositorio}.
+ **AWS_ACCOUNT_ID:** ID de la cuenta de AWS.
+ **AWS_REGION:** Región de la cuenta de AWS.
+ **AWS_ROLE_TO_ASSUME:** Nombre del rol IAM para Github Actions.
+ **AWS_LAMBDA_FUNCTION_NAME:** Nombre de la función lambda a invocar para el entrenamiento del modelo.
+ **MLFLOW_TRACKING_URI:** URI del servidor de MLFlow en la forma de
http://\<Public_IP/Domain_Name\>:\<Port\>.
+ **MODEL_S3_BUCKET:** Nombre de la bucket de registro de modelos.

## Integración con MLFlow
MLFlow es una plataforma y framework de código abierto diseñada para facilitar el desarrollo en conjunto de agentes de inteligencia artificial, machine learning y LLMs. Es usada para llevar el registro de las metricas, parametros de entrenamiento y control de los experimentos.

Para integrar MLFlow a un proyecto de python, siga el siguiete formato:
```
# train.py
import mlflow
import mlflow.<LibreríaML>
# Otros imports necesarios

# Indica a MLFlow en que experimento se está trabajando.
# Los experimentos son definidos por el administrador/jefe de 
# investigación. Si el experimento no existe, MLFlow dará un error.
mlflow.set_experiment("vil20776-torch-mlops-example-project")

# Realice cualquier preparativo necesario para el modelo.

with mlflow.start_run():

    # Puede desarrollar el modelo apartir de aquí.

    # Al finalizar puede hacer uso de funciones como
    # mlflow.log_param(param, value), mlflow.log_metric(name, value),
    # entre otras para llevar registros de los estrenamientos.

    # Finalmente guarde el modelo en MLFlow usando:
    # mlflow.<LibreríaML>.log_model(model)
```
Consulte la documentación de [seguimiento con MLFlow](https://mlflow.org/docs/latest/ml/tracking/) para más detalles.