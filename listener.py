from flask import Flask, request, jsonify
import configparser, sys
from loguru import logger
import logging.handlers
from pathlib import Path

from sms_sender import SmsManager

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        'service_name': 'SMSer gateway',
        'version': '0.0.1'
    })

@app.route("/sms/send", methods=["POST"])
def result():
    token = request.headers.get('Authorization')

    if token == conf_token:
        logger.info('Token correct')

        try:
            resp_json = request.get_json()
            tags = resp_json['tags']
            phone_groups = dict(config.items())

            logger.debug(resp_json)
            logger.debug(tags)
            logger.debug(phone_groups)

            for group in tags:
                if group in phone_groups:
                    message = resp_json['title'] + ' | ' + resp_json['message']

                    phone_numbers = dict(config.items(group))

                    for nr in phone_numbers.values():
                        sms.send(nr, message)

                else:
                    logger.warning("Can not find {x} group in config file.", x=group )

            return True

        except:
            logger.exception('Invalid json body')
            logger.debug(request)
    else:
        logger.critical('Invalid token')
        return ''


if __name__ == '__main__':

    # Load configuration from conf.cnf __file__
    config_path = Path(__file__).resolve().parent.joinpath('conf.cnf')

    config = configparser.ConfigParser()
    config.readfp(open(config_path))
    conf_token = config.get('security', 'token')
    SYSLOG_SRV_IP = config.get('syslog', 'remote_srv')
    SYSLOG_UDP_PORT = config.get('syslog', 'port')
    LOG_LEVEL = config.get('logger', 'LOGLEVEL')
    LOG_FILE = config.get('logger', 'LOGFILE')

    # Logging settings
    logger.propagate = False
    config = {
        "handlers": [
            {"sink": LOG_FILE, 'level': LOG_LEVEL, 'rotation':"01:00"},
            {"sink": sys.stdout, 'format':"<green>{time}</green> <level>{message}</level>"}
        ]
    }
    logger.configure(**config)

    # Send to syslog
    handler = logging.handlers.SysLogHandler(address=(SYSLOG_SRV_IP, SYSLOG_UDP_PORT))
    logger.add(handler, format="<green>{time}</green> <level>{message}</level>", level=LOG_LEVEL)

    #SMS class
    sms = SmsManager()

    logger.success('Server started')
    app.run(host='0.0.0.0', port=80)
