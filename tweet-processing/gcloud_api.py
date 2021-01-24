"""Functions for interfacing with Google Cloud ML models"""

from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account
from google.cloud import automl_v1
from google.cloud import language_v1


def stock_tweet_classifier(tweet_string, model_name):
    """Passes tweet into trained AutoML model, outputs classification on whether it is stock-related"""

    options = ClientOptions(api_endpoint='automl.googleapis.com')
    credentials = service_account.Credentials.from_service_account_file('AutoMLAuth.json')
    prediction_client = automl_v1.PredictionServiceClient(client_options=options, credentials=credentials)

    text_snip = {'text_snippet': {'content': tweet_string, 'mime_type': 'text/plain'}}
    payload = automl_v1.ExamplePayload(text_snip)
    # print(payload)
    request = prediction_client.predict(name=model_name, payload=payload)

    return request