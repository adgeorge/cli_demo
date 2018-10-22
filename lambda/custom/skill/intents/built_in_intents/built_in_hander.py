from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def help_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speach_text = "You can ask me facts about Tensor I. O. T. What would you like to know?"
    print_text = "You can ask me facts about TensorIoT. What would you like to know"
    title = "TensorIoT"

    handler_input.response_builder.ask(speach_text).set_card(SimpleCard(title=title, content=print_text)).\
        set_should_end_session(False)

    return handler_input.response_builder.response


def cancel_and_stop_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text))
    return handler_input.response_builder.response


def session_ended_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    # any cleanup logic goes here

    return handler_input.response_builder.response


def all_exception_handler(handler_input, exception):
    # type: (HandlerInput, Exception) -> Response
    # Log the exception in CloudWatch Logs
    print(exception)

    speech = "Sorry, I didn't get it. Can you please say it again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response
