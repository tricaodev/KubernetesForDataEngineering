# KubernetesForDataEngineering
## 1. Target
### Using Kubernetes to automate DAG Airflow deployment, monitoring, and management for data engineering
## 2. How to run app
### 2.1. Install docker desktop
### 2.2. Enable Kubernetes in docker desktop
### 2.3. Install kubectl and helm
### 2.4. Create Kubernetes Dashboard
* ```kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml```
* ```kubectl proxy```
* Launch to ```http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login```
### 2.5. Generate access token for kubernetes dashboard
* ```kubectl apply -f dashboard-adminuser.yaml```
* ```kubectl apply -f dashboard-clusterrole.yaml```
* ```kubectl apply -f dashboard-secret.yaml```
* ```kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d```
### 2.6. Install airflow
* ```helm install airflow apache-airflow/airflow -n airflow --create-namespace --debug -f values.yaml```
* ```kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow```
* Launch to ```localhost:8080``` with ```user=admin;password=admin```
* Review DAG in Apache Airflow