# Integración con MLFlow
MLFlow es una plataforma y framework de código abierto diseñada para facilitar el desarrollo en conjunto de agentes de inteligencia artificial, machine learning y LLMs. Es usada para llevar el registro de las metricas, parametros de entrenamiento y control de los experimentos.

Para integrar MLFlow a un proyecto de python, el código de entrenamiento de seguir la siguiente estructura:
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

# Esta linea define cuando mlflow puede iniciar el monitoreo.
# Para probar multiples configuraciones solo agregue un nuevo 
# bloque de código que inicie con esta linea.
with mlflow.start_run():

    # Puede desarrollar la configuración y entrenamiento del 
    # modelo apartir de aquí.

    # Al finalizar puede hacer uso de funciones como
    # mlflow.log_param(param, value), mlflow.log_metric(name, value),
    # entre otras para llevar registros de los estrenamientos.

    # Finalmente guarde el modelo en MLFlow usando:
    # mlflow.<LibreríaML>.log_model(model)
```
Para más detalles, consulte los siguientes recursos de MLFlow:
+ [MLFlow Tracking](https://mlflow.org/docs/latest/ml/tracking/)
+ [MLFlow Tracking APIs](https://mlflow.org/docs/latest/ml/tracking/tracking-api/)
+ [MLFlow Models](https://mlflow.org/docs/latest/ml/model/)
+ [MLFlow Python API](https://mlflow.org/docs/latest/api_reference/python_api/index.html)