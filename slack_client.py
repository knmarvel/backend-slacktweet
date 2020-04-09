#!/usr/bin/env python3
"""
A standalone Slack client implementation
see https://slack.dev/python-slackclient/
"""
import os
import sys
from slack import RTMClient, WebClient
from dotenv import load_dotenv
import logging.config
import logging
import yaml
import shlex
# Guard against python2

if sys.version_info[0] < 3:
    raise RuntimeError("Please use Python 3")

load_dotenv()

# globals
BOT_NAME = "zuschauer-bot"
BOT_CHAN = "#bot-test"
bot_commands = {
    'help':  'Shows this helpful command reference.',
    'ping':  'Show uptime of this bot.',
    'exit':  'Shutdown the entire bot (requires app restart)',
    'quit':  'Same as exit.',
    'list':  'List current twitter filters and their counters',
    'add':  'Add some twitter keyword filters.',
    'del':  'Remove some twitter keyword filters.',
    'clear':  'Remove all twitter filters',
    'raise':  'Manually test exception handler'
}

# Create module logger from config file
def config_logger():
    """Setup logging configuration"""
    with open('logging.yaml') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    return logging.getLogger(__name__)
    
logger = config_logger()

class SlackClient:
    def __init__(self, bot_user_token, bot_id=None):
        self.name = BOT_NAME
        self.bot_id = bot_id
        if not self.bot_id:
            # Read the bot's id by calling auth.test
            response = WebClient(token=bot_user_token).api_call('auth.test')
            self.bot_id = response['user_id']
            logger.info(f"My bot_id is {self.bot_id}")
        self.sc = RTMClient(token=bot_user_token, run_async=True)
        # Connect our callback events to the RTM client
        RTMClient.run_on(event="hello")(self.on_hello)
        RTMClient.run_on(event="message")(self.on_message)
        RTMClient.run_on(event="goodbye")(self.on_goodbye)
        # startup our client event loop
        self.future = self.sc.start()
        self.at_bot = f'<@{self.bot_id}>'
        logger.info("Created new SlackClient Instance")
    def __repr__(self):
        return self.at_bot
    def __str__(self):
        return self.__repr__()
    def on_hello(self, **payload):
        """Slack has confirmed our connection request"""
        logger.info(f'{self} is connected to Slack RTM server.')
        self.post_message(f'{self.name} is now online')
    def on_message(self, **payload):
        """Slack has sent a message to me"""
        data = payload['data']
        if 'text' in data and self.at_bot in data['text']:
            # parse everything after the <@bot> mention
            raw_cmd = data['text'].split(self.at_bot)[1].strip().lower()
            chan = data['channel']
            # now it's time to handle the command
            response = self.handle_command(raw_cmd, chan)
            self.post_message(response, chan)
    def handle_command(self, raw_cmd, chan):
        """Parses a raw command string directed at our bot"""
        response = None
        args = shlex.split(raw_cmd)
        cmd = args[0].lower()
        logger.info(f'{self} Received command: "{raw_cmd}"')
        if cmd not in bot_commands:
            response = f'Unknown command: "{cmd}"'
            logger.error(f'{self} {response}')
        # Now we have a valid cmd that we must process
        elif cmd == 'help':
            pass
        elif cmd == 'ping':
            pass
        elif cmd == 'list':
            pass
        return response
    def on_goodbye(self, **payload):
        logger.warning(f"{self} is disconnecting now")
    def post_message(self, msg, chan=BOT_CHAN):
        """Sends a message to a slack channel"""
        # MAKE SURE THAT ... we have a actual WebClient instance
        assert self.sc._web_client is not None
        if msg:
            self.sc._web_client.chat_postMessage(
                channel=chan,
                text=msg
            )
    def run(self):
        logger.info("Waiting for things to happen ...")
        loop = self.future.get_loop()
        # Wait forever
        loop.run_until_complete(self.future)
        logger.info("Done waiting for things.  done-DONE!")
def main(args):
    SlackClient(
        os.environ['BOT_USER_TOKEN'],
        os.environ['BOT_USER_ID']
    ).run()
if __name__ == '__main__':
    main(sys.argv[1:])
    logger.info("Completed.")
