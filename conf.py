# conf.py
import os
from google.cloud import secretmanager

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.getenv('GCP_PROJECT_ID')}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

# Load secrets
stripe_secret_key = get_secret("STRIPE_SECRET_KEY")
sqlalchemy_database_url = get_secret("SQLALCHEMY_DATABASE_URL")

# Set environment variables
os.environ["STRIPE_SECRET_KEY"] = stripe_secret_key
os.environ["SQLALCHEMY_DATABASE_URL"] = sqlalchemy_database_url