import mlflow
from mlflow.tracking import MlflowClient

# Define the custom headers
headers = {
    "Authorization": "Bearer your_auth_token_here"
}

# Create an MlflowClient with the custom headers
client = MlflowClient(tracking_uri="https://your_tracking_server", headers=headers)

# Use the client for your operations
client.log_param("your_run_id", "param1", 5)
client.log_metric("your_run_id", "metric1", 0.89)
