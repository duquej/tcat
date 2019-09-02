import routelogic

#Core Skill Functionality

"""Gets the origin and destination values from the json returned by Alexa """
def getValues(event, context):
    originValue = event['request']['intent']['slots']['origin']['value']
    destValue = event['request']['intent']['slots']['destination']['value']
    values = [originValue,destValue]
    return values



# Builders

"""Builds the plain speech text that alexa will utter """
def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

"""Creates the reponse format """
def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response

"""Creates a card that will be used to assemble the utterance """
def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card


# Responses

"""Builds the utterance that alexa will tell the user """
def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet)
    
"""Once the user is ready to stop the skill; this function will essentially 'shutdown' the skill """
def stopIntent(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)


# Custom Intents

"""Contains the main functionality for finding the next bus route to the users requested destination """
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

# Required Intents

def cancel_intent():
    return statement("CancelIntent", "You want to cancel" 


def help_intent():
    return statement("CancelIntent", "You want help")		


def stop_intent():
    return stopIntent("StopIntent", "Thanks for using our skill!")		


# On launch
"""When the skill first loads, this is what alexa will tell the user """
def on_launch(event, context):
    return statement("start", "Welcome to the Ithaca Bus Skill. Please tell me where you want to go and where you are.")


# Routing

"""Retrieves the intent that the user requested """"
def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom intents
    
    
    if intent == "getroute":
        return getRoute(event,context)
        

    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()


"""Program Entry, filters the users requested action """"
def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
