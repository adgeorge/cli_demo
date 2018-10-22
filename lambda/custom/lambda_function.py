from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from skill.intents.testing_intent.testing_handler import testing_handler
from skill.intents.company_fact_intent.company_fact_handler import company_fact_handler
from skill.intents.employee_fact_intent.employee_fact_handler import employee_fact_handler
from skill.intents.built_in_intents.built_in_hander import cancel_and_stop_intent_handler, all_exception_handler, \
    session_ended_request_handler, help_intent_handler
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


# INTENTS
@sb.request_handler(can_handle_func=is_intent_name("CompanyFact"))
def company_fact_intent(handler_input):
    return company_fact_handler(handler_input)


@sb.request_handler(can_handle_func=is_intent_name("EmployeeFact"))
def employee_fact(handler_input):
    return employee_fact_handler(handler_input)


@sb.request_handler(can_handle_func=is_intent_name("Testing"))
def testing_intent(handler_input):
    return testing_handler(handler_input)


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_intent(handler_input):
    return session_ended_request_handler(handler_input)


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent(handler_input):
    return help_intent_handler(handler_input)


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent(handler_input):
    return cancel_and_stop_intent_handler(handler_input)


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_intent(handler_input, exception):
    return all_exception_handler(handler_input, exception)


lambda_handler = sb.lambda_handler()
