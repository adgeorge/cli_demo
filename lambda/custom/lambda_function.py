from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s]: %(asctime)s | '
                           '[PATH]: %(filename)s: %(funcName)s(), line:%(lineno)d) | '
                           '[MESSAGE]: %(message)s')
logger = logging.getLogger()
handler = logger.handlers[0]
formatter = logging.Formatter('[%(levelname)s] | '
                              '[MESSAGE]: %(message)s | '
                              '[NAME]: %(name)s | '
                              '[PATH]: %(filename)s: %(funcName)s(), line:%(lineno)d) | '
                              '[TIME]: %(asctime)s |')
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)


sb = SkillBuilder()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to Tensor i.o.t. <break strength='strong'/> What would you like to know about?"
    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("EmployeeFact"))
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


# @login_required
# @sb.request_handler(can_handle_func=is_intent_name("EmployeeSecretFact"))
# def employee_secret_fact_handler(handler_input):
#     # type: (HandlerInput) -> Response
#     employee = handler_input.request_envelope.request.intent.slots['employee'].value
#     logger.debug("Employee Value: {}".format(employee))
#
#     status_code = handler_input.request_envelope.request.intent.slots['employee'].resolutions. \
#         resolutions_per_authority[0].status.code.value
#     logger.debug("status_code: {}".format(status_code))
#
#     if status_code == "ER_SUCCESS_MATCH":
#         secret_fact = get_employee_secret_fact()
#         speech_text = "{} is awesome at being awesome!".format(employee)
#     elif status_code == "ER_SUCCESS_NO_MATCH":
#         speech_text = "{} does not work at Tensor i.o.t.".format(employee)
#     else:
#         speech_text = "Who would you like to know about?"
#     handler_input.response_builder.speak(speech_text)\
#         .set_card(SimpleCard(title=employee.title(), content=speech_text)).\
#         set_should_end_session(None)
#
#     return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("CompanyFact"))
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


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speach_text = "You can ask me facts about Tensor I. O. T. What would you like to know?"
    print_text = "You can ask me facts about TensorIoT. What would you like to know"
    title = "TensorIoT"

    handler_input.response_builder.ask(speach_text).set_card(SimpleCard(title=title, content=print_text)).\
        set_should_end_session(False)

    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Hello World", speech_text))
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    # any cleanup logic goes here

    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # type: (HandlerInput, Exception) -> Response
    # Log the exception in CloudWatch Logs
    print(exception)

    speech = "Sorry, I didn't get it. Can you please say it again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


lambda_handler = sb.lambda_handler()
