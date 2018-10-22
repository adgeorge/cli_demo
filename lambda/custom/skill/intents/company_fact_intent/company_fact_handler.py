from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.utils import is_request_type, is_intent_name
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def company_fact_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Tensor I. O. T. was founded by C. E. O. Ravi Raghunathan in September 2017."
    print_text = "TensorIoT was founded by CEO Ravi Raghunathan in September 2017."
    title = "TensorIoT"
    response_builder = handler_input.response_builder

    response_builder.set_card(
        SimpleCard(title=title, content=print_text)
    )

    response_builder.speak(speech_text)
    return handler_input.response_builder.response