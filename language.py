import httplib2, grequests, sys
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def process_message(message):
    pass

def prob_interrogative(sentence):
    """ Determine likelihood of sentence being interrogative.
    Returns value between 0 and 1.
    """
    prob = 0
    # Plan to apply ML Classification. For now just simple implementation.
    # If sentence includes 5w1h +0.4
    # If 5w+1h is beginning of sentence +0.2
    # If sentence ends with "?", +0.4
    wh = ['what','where','which','who','when','how']
    if any(str in sentence.lower().strip() for str in wh):
        prob += 0.4
    if any(sentence.lower().strip().startswith(str) for str in wh):
        prob += 0.2
    if "?" in sentence:
        prob += 0.4
    return prob

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
