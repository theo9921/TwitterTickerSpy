"""Functions for interfacing with Google Cloud ML models"""

from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account
from google.cloud import automl_v1
from google.cloud import language_v1


def stock_tweet_classifier(tweet_string):
    """Passes tweet into trained AutoML model, outputs classification on whether it is stock-related"""

    options = ClientOptions(api_endpoint='automl.googleapis.com')
    model_name = 'projects/313817029040/locations/us-central1/models/TCN8645127876691099648'
    credentials = service_account.Credentials.from_service_account_file('AutoMLAuth.json')
    prediction_client = automl_v1.PredictionServiceClient(client_options=options, credentials=credentials)

    text_snip = {'text_snippet': {'content': tweet_string, 'mime_type': 'text/plain'}}
    payload = automl_v1.ExamplePayload(text_snip)
    # print(payload)
    request = prediction_client.predict(name=model_name, payload=payload)

    classification = request.payload[0].display_name

    if classification == 'stock':
        return True
    else:
        return False

def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """
    credentials = service_account.Credentials.from_service_account_file('AutoMLAuth.json')
    client = language_v1.LanguageServiceClient(credentials=credentials)

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

        # Score encoding
        if sentence.sentiment.score <= 0:
            return False
        else:
            return True

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))