#### The file contains some commands how to build the container with the api and examples how to use it.

The command to build the Docker image
```console
docker build -t otus-02-fastapi .
```
The command to start serving
```console
docker run -d --name otus-02-fastapi -p 8080:8080 otus-02-fastapi
```

Some examples how to use:
You need to pass all or some parameters of the patient to get the predict of disease:
```console
curl -X 'GET'   'http://127.0.0.1:8080/predict?age=53&sex=Male&dataset=VA%20Long%20%Beach&cp=asymptomatic&trestbps=154.0&restecg=st-t%20abnormality&thalch=140.0&exang=true&oldpeak=1.5&slope=flat'
```
```console
curl -X 'GET'   'http://127.0.0.1:8080/predict?age=53&sex=Male&dataset=VA%20Long%20%Beach&cp=asymptomatic&trestbps=154.0&chol=230&fbs=false&restecg=normal&thalch=150&exang=false&oldpeak=0.1&slope=downsloping'
```
Prediction will be in json format and will contain the predicted class of the disease according to the classes in train data:
```json
{"prediction":0}
```






