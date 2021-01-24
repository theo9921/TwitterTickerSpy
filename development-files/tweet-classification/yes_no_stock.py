import sys
from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account
from google.cloud import automl_v1
from google.cloud import language_v1

# https://googleapis.dev/python/google-api-core/latest/auth.html
# client = datastore.Client()
credentials = service_account.Credentials.from_service_account_file('rapid-hall-302622-7d92a5d1344e.json')
#client = automl.AutoMlClient(credentials=credentials)


# Function for reading txt file for prediction
def inline_text_payload(file_path):
    with open(file_path, 'rb') as ff:
        content = ff.read()
    return {'text_snippet': {'content': content, 'mime_type': 'text/plain'}}


def get_prediction(file_path, model_name):
    options = ClientOptions(api_endpoint='automl.googleapis.com')
    prediction_client = automl_v1.PredictionServiceClient(client_options=options, credentials=credentials)

    text_snip = inline_text_payload(file_path)
    #text_snip = {'text_snippet': {'content': "this is some test string", 'mime_type': 'text/plain'}}
    payload = automl_v1.ExamplePayload(text_snip)
    print(payload)
    request = prediction_client.predict(name=model_name, payload=payload)
    return request  # waits until request is returned


print(get_prediction('stock_tweets/y_5.txt', 'projects/313817029040/locations/us-central1/models/TCN8645127876691099648'))