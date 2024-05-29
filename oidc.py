import requests
import mlflow
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.util.retry import Retry

SERVICE = "your_service_url"
PORT = "your_service_port"
USERNAME = "admin@kubeflow.org"
PASSWORD = "12341234"

# Step 0: Initial request to get the authentication URL
response = requests.get(f"http://{SERVICE}:{PORT}")
state_value = response.url.split('state=')[-1]

# Step 1: Get the REQ_VALUE
response = requests.get(f"http://{SERVICE}:{PORT}/dex/auth?client_id=kubeflow-oidc-authservice&redirect_uri=%2Flogin%2Foidc&response_type=code&scope=profile+email+groups+openid&state={state_value}")
req_value = response.url.split('req=')[-1]

# Step 2: Post login credentials
data = {
    'login': USERNAME,
    'password': PASSWORD
}
response = requests.post(f"http://{SERVICE}:{PORT}/dex/auth/local?req={req_value}", data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

# Step 3: Approve the authentication request
response = requests.get(f"http://{SERVICE}:{PORT}/dex/approval?req={req_value}")
code_value = response.url.split('code=')[-1].split('&')[0]

# Step 4: Get the session cookie
response = requests.get(f"http://{SERVICE}:{PORT}/login/oidc?code={code_value}&state={state_value}")
session_cookie = response.cookies.get('authservice_session')

# Create a custom session with retries and attach the session cookie
session = Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.cookies.set('authservice_session', session_cookie)

# Use this session for MLflow HTTP requests
def mlflow_request(method, url, **kwargs):
    response = session.request(method, url, **kwargs)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response

# Set the tracking URI using the custom session
mlflow.set_tracking_uri(f"http://{SERVICE}:{PORT}")

# Define a custom MLflow client to use the session for API calls
class CustomMlflowClient(mlflow.tracking.MlflowClient):
    def __init__(self, tracking_uri=None):
        super().__init__(tracking_uri)
        self._tracking_uri = tracking_uri

    def _tracking_request(self, method, endpoint, params=None, data=None, json=None, headers=None):
        url = f"{self._tracking_uri}{endpoint}"
        return mlflow_request(method, url, params=params, data=data, json=json, headers=headers)

# Instantiate the custom client
client = CustomMlflowClient(tracking_uri=f"http://{SERVICE}:{PORT}")

# Create or set the experiment
experiment_name = "your_experiment_name"
client.create_experiment(experiment_name)
mlflow.set_experiment(experiment_name)

# Start a new MLflow run
with mlflow.start_run():
    # Log a parameter
    mlflow.log_param("param1", 5)
    # Log a metric
    mlflow.log_metric("metric1", 0.89)

print("Logged data to MLflow")
