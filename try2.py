from langchain.agents import create_json_agent
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.tools.json.tool import JsonSpec
import json

file = "faqs.json"
with open(file, "r") as f1:
    data = json.load(f1)
    f1.close()

from google.cloud import aiplatform

# Replace with your project ID, API key, and region
project_id = "your-project-id"
region = "asia-south1"
api_key = "your-api-key"

# Initialize the client
client = aiplatform.gapic.PredictionServiceClient(
    credentials=aiplatform.credentials.from_service_account_json(
        f"path/to/your/service-account-key.json"
    )
)

# Set the endpoint and model name
endpoint = f"https://{region}-aiplatform.googleapis.com/"
model_name = "projects/your-project-id/locations/asia-south1/models/your-model-name"

# Create the request
request = aiplatform.gapic.types.PredictRequest(
    endpoint=endpoint, model_name=model_name, instances=[{"text": "Hello, world!"}]
)

# Make the request
response = client.predict(request)

# Print the response
print(response.predictions)spec = JsonSpec(dict_=data, max_value_length=4000)
toolkit = JsonToolkit(spec=spec)

