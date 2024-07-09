import requests

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
