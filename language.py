import httplib2, grequests, sys
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def process_message(message):
    pass



########################
# Natural Language API #
########################

def analyze_syntax(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'features': {
            'extract_syntax': True,
        },
        'encodingType': encoding,
    }

    service = get_service()

    request = service.documents().annotateText(body=body)
    response = request.execute()

    return response


def analyze_all(text):
    
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'features': {
            'extractSyntax': True,
            'extractEntities' : True,
            'extractDocumentSentiment' : True
        },
        'encodingType': get_native_encoding_type(),
    }

    service = get_service()

    request = service.documents().annotateText(body=body)
    response = request.execute()

    return response
    


def analyze_sentiment(text):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        }
    }

    service = get_service()

    request = service.documents().analyzeSentiment(body=body)
    response = request.execute()

    return response

def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def get_service():
    """ Auth with  Google Natural Languagge API """
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    return discovery.build('language', 'v1beta1', http=http)
