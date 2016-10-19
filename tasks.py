import celery, os, requests, json
import language

_post_msg_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+os.environ['FBOT_ACCESS_TOKEN']


app = celery.Celery('buck')
#app.conf.update(BROKER_URL=os.environ['REDIS_URL'], CELERY_RESULT_BACKEND=os.environ['REDIS_URL'], BROKER_POOL_LIMIT=0)
app.conf.update(BROKER_URL=os.environ['CLOUDAMQP_URL'],BROKER_POOL_LIMIT=20)


##########
# Celery #
##########

@app.task
def add(x,y):
    print 'testing add'
    return x+y

@app.task
def process(data):
    if 'message' in data['entry'][0]['messaging'][0]: # The 'messaging' array may contain multiple messages.  Need fix.
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']
        analysis = language.analyze_sentiment(message)
        analysis_res = json.dumps(analysis)
        print "test result:"
        print analysis_res
        print "Analyze All:"
        print json.dumps(language.analyze_all(message))
        # sending messages will be moved out of this module.
        resp_data = {
            "recipient" : {"id":sender_id},
            "message" : {"text":message+' : '+analysis_res}        
        }
        print 'POST RESPONSE BACK TO: '+ _post_msg_url
        post_result = requests.post(_post_msg_url, json=resp_data)
        print post_result
    return

def firebase_save_user_msg(user_id, msg):
    """ Save data to Firebase
    Keyword arguments:
    user_id -- 
    msg -- 
    """
    pass

def http_send(reqs_array):
    """ Async HTTP requests using grequests
    """
    pass


