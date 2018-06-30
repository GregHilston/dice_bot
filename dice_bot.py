import csv
import os
from logging.config import dictConfig
from simple_slack_bot.simple_slack_bot import SimpleSlackBot

PATH = os.path.dirname(os.path.realpath(__file__))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'rotate': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(PATH, 'logs/dnd.log'),
            'when': 'midnight',
            'backupCount': 7,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate'],
            'level': 'INFO'
        }
    }
}
dictConfig(LOGGING)

simple_slack_bot = SimpleSlackBot(debug=True)

users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = simple_slack_bot.helper_user_id_to_user_name(uid)
    return users[uid]

@simple_slack_bot.register("message")
def roll_callback(request):
    """This function is called every time a message is sent to a channel out Bot is in
    :param request: the SlackRequest we receive along with the event. See the README.md for full documentation
    :return: None
    """

    fields = []

    if "CBGJ4P2JJ" != request.channel:
        return

    # player message
    if request._slack_event.event.get("subtype") == "me_message":
            fields.append("Player")
            fields.append(get_user(request.user))
            fields.append(request.message)

    # DM message
    elif request.message.startswith("&gt;"):
            fields.append("DM")
            fields.append(get_user(request.user))
            fields.append(request.message)

    if fields:
        with open(r"transcript.csv", 'a') as transcript:
            writer = csv.writer(transcript)
            writer.writerow(fields)

def main():
    simple_slack_bot.start()


if __name__ == "__main__":
    main()
