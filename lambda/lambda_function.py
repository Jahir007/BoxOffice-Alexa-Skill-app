# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import random
import requests
import json
import os

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_model import Response
from ask_sdk_model.ui import SsmlOutputSpeech
from ask_sdk_model.interfaces.audioplayer import PlayDirective, PlayBehavior
from ask_sdk-_core.skill_builder import CustomSkillBuilder
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Define persistence adapter
SKILL NAME='BoxOffice'
ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
ddb_resource = boto3.resource('dynamodb' region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)
sb = CustomerSkillBuilder(persistence_adapter=dymanodb_adapter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import random
import boto3
import os
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler, AbstractResponseInterceptor
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SsmlOutputSpeech
from ask_sdk_model.response import Response
from ask_sdk_model.services import ServiceException

sb = SkillBuilder()
polly_client = boto3.client('polly')

# define speechcon phrases to add more personality to the responses
speechcons = ["Bazinga!", "Kaboom!", "Ta-da!", "Aloha!", "Oh snap!", "Booyah!"]

# define the movie genres available for recommendation
movie_genres = ["action", "romantic comedy", "horror", "drama", "documentary", "science fiction"]

# define the celebrities available for news updates
celebrities = ["Kim Kardashian", "Brad Pitt", "Taylor Swift", "Jennifer Aniston", "George Clooney"]

# define the sound effects available for box office updates
sound_effects = ["applause_3.mp3", "gong.mp3", "fanfare.mp3", "tada.mp3", "crowd_cheering.mp3"]

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech = "Welcome to the Movie Recommendation, Celebrity News and Box Office Updates Skill. " \
                 "You can ask me for a movie recommendation, celebrity news or box office updates. " \
                 "What would you like to do?"
        reprompt = "What would you like to do?"
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

class MovieRecommendationsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("MovieRecommendationsIntent")(handler_input)

    def handle(self, handler_input):
        genre = random.choice(movie_genres)
        speech = f"Here's a {genre} movie recommendation for you. "
        if genre == "action":
            speech += "I recommend watching Mission: Impossible - Fallout. It's a thrilling action movie with lots of " \
                      "excitement and great stunts."
        elif genre == "romantic comedy":
            speech += "I suggest watching Crazy Rich Asians. It's a charming romantic comedy with great characters and " \
                      "a heartwarming story."
        elif genre == "horror":
            speech += "I recommend watching Hereditary. It's a bone-chilling horror movie with a great cast and " \
                      "terrifying scares."
        elif genre == "drama":
            speech += "I suggest watching The Shape of Water. It's a beautiful and poignant drama with stunning " \
                      "visuals and a great performance by Sally Hawkins."
        elif genre == "documentary":
            speech += "I recommend watching Blackfish. It's a powerful documentary about the treatment of killer " \
                      "whales in captivity and their impact on the people who work with them."
        else:
            speech += "I suggest watching Blade Runner 2049. It's a stunning science fiction movie with amazing " \
                      "visual effects and a great story."
        # add a speechcon to the response
        speech += "<say-as interpret-as='interjection'>" + random.choice(speechcons) + "!</say-as>"
        handler_input.response_builder.speak(speech).set_should_end_session(True)
        return handler_input.response_builder.response
class CelebrityNewsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("CelebrityNewsIntent")(handler_input)

    def handle(self, handler_input):
        celebrity = random.choice(celebrities)
        speech = f"Here's the latest news about {celebrity}. "
        try:
            # use the Bing Search API to get the latest news about the celebrity
            bing_search = boto3.client('secretsmanager').get_secret_value(SecretId='bing_search')
            search_key = json.loads(bing_search['SecretString'])['api_key']
            search_url = f"https://api.cognitive.microsoft.com/bing/v7.0/news/search?q={celebrity}&count=1&freshness=Day"
            headers = {"Ocp-Apim-Subscription-Key": search_key}
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                news = response.json()['value'][0]['description']
                speech += news
            else:
                speech += "I'm sorry, I couldn't find any news about that celebrity at the moment."
        except (ServiceException, KeyError, IndexError):
            speech += "I'm sorry, I couldn't find any news about that celebrity at the moment."
        # add a speechcon to the response
        speech += "<say-as interpret-as='interjection'>" + random.choice(speechcons) + "!</say-as>"
        handler_input.response_builder.speak(speech).set_should_end_session(True)
        return handler_input.response_builder.response
class BoxOfficeUpdatesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BoxOfficeUpdatesIntent")(handler_input)

    def handle(self, handler_input):
        sound_effect = random.choice(sound_effects)
        speech = "Here are the latest box office updates. "
        try:
            # use the OMDB API to get the top-grossing movie of the week
            omdb = boto3.client('secretsmanager').get_secret_value(SecretId='omdb')
            omdb_key = json.loads(omdb['SecretString'])['api_key']
            omdb_url = f"http://www.omdbapi.com/?apikey={omdb_key}&type=movie&s=&y=&r=json"
            response = requests.get(omdb_url)
            if response.status_code == 200:
                movies = response.json()['Search']
                top_grossing = max(movies, key=lambda movie: float(movie['imdbRating']))
                title = top_grossing['Title']
                box_office = top_grossing['BoxOffice']
                speech += f"The top-grossing movie of the week is {title}, which has made {box_office} at the box office."
            else:
                speech += "I'm sorry, I couldn't get the latest box office updates at the moment."
        except (ServiceException, KeyError, IndexError):
            speech += "I'm sorry, I couldn't get the latest box office updates at the moment."
            
            
            
        # add a sound effect to the response
        directive = {
            "type": "Alexa.Presentation.APL.Audio",
            "version": "1.0",
            "durationsInMilliseconds": [3000],
            "audioTrack": "foreground",
            "source": sound_effect
        }
        handler_input.response_builder.add_directive(directive)
        # add a speechcon to the response
        speech += "<say-as interpret-as='interjection'>" + random.choice(speechcons) + "!</say-as>"
        handler_input.response_builder.speak(speech).set_should_end_session(True)
        return handler_input.response_builder.response


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()