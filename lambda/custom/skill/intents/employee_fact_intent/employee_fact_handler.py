from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def employee_fact_handler(handler_input):
    # type: (HandlerInput) -> Response

    employee = handler_input.request_envelope.request.intent.slots['employee'].value
    logger.debug("Employee Value: {}".format(employee))

    status_code = handler_input.request_envelope.request.intent.slots['employee'].resolutions. \
        resolutions_per_authority[0].status.code.value
    logger.debug("status_code: {}".format(status_code))

    if status_code == "ER_SUCCESS_MATCH":
        employee = employee.lower()
        speech_text = "{} is awesome at being awesome!".format(employee)
    elif status_code == "ER_SUCCESS_NO_MATCH":
        speech_text = "{} does not work at Tensor i.o.t.".format(employee)
    else:
        speech_text = "Who would you like to know about?"
    handler_input.response_builder.speak(speech_text)\
        .set_card(SimpleCard(title=employee.title(), content=speech_text)).\
        set_should_end_session(None)

    return handler_input.response_builder.response