from google.oauth2 import service_account
from google.cloud import automl
from google.cloud import language_v1

# https://googleapis.dev/python/google-api-core/latest/auth.html
#client = datastore.Client()
credentials = service_account.Credentials.from_service_account_file('rapid-hall-302622-bc1821ff2bd1.json')
client = automl.AutoMlClient(credentials=credentials)


