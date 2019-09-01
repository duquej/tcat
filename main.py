import routelogic
###########################
#CORE SKILL FUNCTIONALITY
##########################
def getValues(event, context):
    originValue = event['request']['intent']['slots']['origin']['value']
    destValue = event['request']['intent']['slots']['destination']['value']
    values = [originValue,destValue]
    return values


##############################
# Builders
##############################


def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech


def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card


##############################
# Responses
##############################


def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes=session_attributes)


def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet)
    
def stopIntent(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)


def continue_dialog():
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    return build_response(message)


##############################
# Custom Intents
##############################

def SampleIntent(event, context):
        return statement("trip_intent", "sample intent worked")

    
def bus_intent(event, context):
    
    busValue = event['request']['intent']['slots']['route']['value']

    bus = "you want bus " + busValue
    return statement("get_route", bus)


def counter_intent(event, context):
    session_attributes = event['session']['attributes']

    if "counter" in session_attributes:
        session_attributes['counter'] += 1

    else:
        session_attributes['counter'] = 1

    return conversation("counter_intent", session_attributes['counter'],
                        session_attributes)


def trip_intent(event, context):
    dialog_state = event['request']['dialogState']

    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog()

    elif dialog_state == "COMPLETED":
        return statement("trip_intent", "Have a good trip")

    else:
        return statement("trip_intent", "No dialog")

def getRoute(event,context):
    
    values = getValues(event,context)    
    jsonData = routelogic.generateJson(values[0], values[1])
    
    if routelogic.checkErrors(jsonData) != 'OK':
        return statement("error", routelogic.checkErrors(jsonData))
    
    sentenceArgs = routelogic.parseJson(jsonData)
    
    if sentenceArgs[0] == "Failure":
        return statement("error", "No bus route available")

    sentence = routelogic.createInformation(sentenceArgs)
    
    return statement("businfo", sentence)
##############################
# Required Intents
##############################


def cancel_intent():
    return statement("CancelIntent", "You want to cancel")	#don't use CancelIntent as title it causes code reference error during certification 


def help_intent():
    return statement("CancelIntent", "You want help")		#same here don't use CancelIntent


def stop_intent():
    return stopIntent("StopIntent", "Thanks for using our skill!")		#here also don't use StopIntent


##############################
# On Launch
##############################


def on_launch(event, context):
    return statement("start", "Welcome to the Ithaca Bus Skill. Please tell me where you want to go and where you are.")


##############################
# Routing
##############################


def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom Intents
    if intent == "SampleIntent":
        return SampleIntent(event, context)

    if intent == "CounterIntent":
        return counter_intent(event, context)

    if intent == "BusRoute":
        return bus_intent(event, context)

    if intent == "TripIntent":
        return trip_intent(event, context)
    
    if intent == "getroute":
        return getRoute(event,context)
        

    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()


##############################
# Program Entry
##############################


def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
