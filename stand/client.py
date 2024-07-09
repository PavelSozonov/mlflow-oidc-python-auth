import mlflow
from mlflow.utils.rest_utils import http_request

# Define your custom token
custom_token = 'your_token_here'

# Custom request function to add session-id header
def custom_http_request(*args, **kwargs):
    extra_headers = {'session-id': custom_token}
    return http_request(*args, extra_headers = extra_headers, **kwargs)

# Override the default request function
#mlflow.utils.rest_utils.http_request_safe = custom_http_request
mlflow.utils.rest_utils.http_request = custom_http_request

# Set the tracking URI to http://nginx:80
mlflow.set_tracking_uri("http://nginx:80")

# Example usage of Mlflow client with custom headers and tracking URI
with mlflow.start_run():
    mlflow.log_param("param1", 5)
    mlflow.log_metric("metric1", 0.85)

print("Run logged successfully.")
