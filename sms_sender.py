from requests import Session
from zeep.transports import Transport
from zeep import Client
from loguru import logger

import xml.etree.ElementTree as ET


class SmsManager:

    def __init__(self):
        session = Session()
        session.verify = False
        transport = Transport(session=session)

        self.client = Client("https://soap.server.example/sendSms.wsdl", transport=transport)


    def send(self, phone_number, message, user='example user'):
        try:
            # Try to send a sms
            response = self.client.service.Sms(PhoneNumber=phone_number, Message=message, user=user)

            # Looking for an error
            xml_root = ET.fromstring(response)

            for child in xml_root:
                if child.tag == 'some_error_string' and child.text:
                    logger.error('Can not send SMS to {phone_number} cause {error}', phone_number=phone_number, error=child.text)
                    return False

            logger.success('Sent SMS to {phone_number}', phone_number=phone_number)

        except:
            logger.exception('Can not send SMS ')

            return False

        return True
