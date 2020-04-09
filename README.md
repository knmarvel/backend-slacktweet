<table>
<tbody>
<tr>
<td><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Slack_Technologies_Logo.svg/2000px-Slack_Technologies_Logo.svg.png" width="256" height="73" /></td>
<td><span style="font-size: 36pt;">&nbsp;+&nbsp;</span></td>
<td><img src="https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/twitter-python-logos.width-808.jpg" width="204" height="102" /></td>
</tr>
</tbody>
</table>

# SlackTweet: A Team Project in Python 3

This project explores building a Slackbot using Python 3.  Of course there are many third-party platforms out there that can automate the process of creating AI-driven bots. But as emerging software engineers, we understand that by diving deep and exploring the nuts and bolts, we acquire a rich knowledge of how things work which will serve us well in the future, as well as honing our skill set of software best practices.  This is a longer-duration assignment-- you will be researching, planning, and experimenting and task-switching between other activities.  Be sure to allocate sufficient time!

This assignment integrates many concepts that you have learned over the last few weeks.  The goal is to create a slackbot framework that you can take with you to extend, adapt, and reuse in many ways.  You will be connecting your Slackbot to your own personal twitter account, and controlling it with a set of commands.

Yes, there already exists an off-the-shelf [twitter integration](https://slack.com/help/articles/205346227) that you can enable within a Slack workspace.  However, this app is limited in its functionality.  You can only post tweets and retweets from a single account.  No hashtag support.

## Learning Objectives
 - Become comfortable with self-guided API research and experimentation
 - Create, test, deploy, manage a long running program in a cloud environment 
 - Apply best practices in repository structure and virtual environment management
 - Familiarize with OAuth authentication process
 - Learn how to create an integration between two real-world APIs
 - Use multi-threading to create a responsive application

## Goal
The goal is to create a _controllable_, long-running Slackbot that subscribes to various Twitter streams, and republishes those tweets into a channel (or channels) on Slack.  You don't need to send messages from Slack to Twitter - just a Twitter listener.  The Bot will be deployed on your existing Heroku cloud-hosting account.

## Setup - Slack Account
For this assignment, we will be using two separate, private Slack Team accounts.  These accounts are only used by the SE cohorts for this assignment, there are no other users.  The reason for using two separate accounts is because Slack free team accounts limit the number of app integrations to max of 10.  Please use these self sign-up links to create your accounts.  Once you are in, send a message to your instructor to ask for *admin* privilege.  You will need `admin` to create a bot application on the Slack website.

 - [kenziebot.slack.com](https://join.slack.com/t/kenziebot/shared_invite/enQtNDk4NzMxNTcyMTE5LWI0OWRmYjYzNjdkZmRlMmE2NWU3ZTc1OWZlZGFiOTAwNDcwN2MxZjI0MjU4YmU0OTcyMTczNzdmMGNhZjRhMzM) (self sign up link)
 
 - [kenziebot2.slack.com](https://join.slack.com/t/kenziebot2/shared_invite/enQtNDk3MDc3NTE3NDQxLWQ3ZDQ3Mjg5NjBlNjIzNGNlMTFmY2UzZDg2MjZhMDZmMWNlMjZjZGQ3NTNhM2U2OGRiY2E2NDk5NTk5YzExODg)  (self sign up link)
 
After you have signed up on either of these Slack workspaces (and have been granted the 'admin' privilege) you are ready to create your slack app.  Visit the [https://api.slack.com/apps](https://api.slack.com/apps) page and follow the instructions to create an app.  After your app is created, use the configuration menu to:
 - Add a **bot** to your app to allow users to exchange messages with your app
 - Install your app to your workspace.
When you are done, you should have some API tokens.  Copy these tokens into a section in your local `.env` file. You will used these tokens in your Python project to create an RTMClient instance.

## Setup - Twitter Account
You will need to set up a twitter account.  You can use your own existing account, or create a new one.  The important part is to register for _developer API access_.  This is a new requirement since July 2018.  You will need to fill out a short questionnaire about your intended usage of the developer account. Your answers should reflect that you are a student who is learning the Twitter API and you do not intend to post any tweets of any kind.

 - https://developer.twitter.com/en.html
 - <img src="img/twitter_quiz.png" height="360px">

Once you have been approved for developer access, Follow the Twitter documentation on creating an app.  Then use the `Keys and Tokens` tab to generate a pair of Consumer keys, and a pair of Access keys.

<img src="img/Twitter_app.png" width="471" height="211" />

You will use the Consumer and Access keys to communicate with your Twitter account via the API.

## Part A: Minimal Slackbot Client
 - Start with a barebones Slackbot client.  Get the connectivity details of sending and receiving messages worked out, one direction at a time.
 - Install the [slackclient](https://python-slackclient.readthedocs.io/en/latest/) python library in your virtual environment.
 - Connect your app to the KenzieBot workspace as a bot user
 - Send a message to a channel announcing that it is online
 - Wait for and process events/messages in an infinite while-loop
 - Ignore any messages that don't contain a direct `@mention` of your bot name
 - Exit your bot program if you receive an exit message.  For example, if your bot is named `example-bot` then your program should exit gracefully when it receives a slack message such as `@example-bot exit`

## Part B: Minimal Twitter Client
Add Twitter communications:

 - Install the [Tweepy python package](http://www.tweepy.org/) into your project's virtual environment.
 - Make sure you can programmatically log in to your twitter account (using the consumer and access tokens) and retrieve status messages.  
 - Use the [tweepy.StreamListener](https://tweepy.readthedocs.io/en/v3.5.0/streaming_how_to.html#streaming-with-tweepy) class to verify that you can attach to the "Twitter Firehose" and receive tweets that are filtered on certain keywords.
 - You may wish to define a `TwitterClient` class object that inherits from `tweepy.Streamlistener.`

## Part C: The Integration
Create a command and control module that connects both clients.  Be aware that there won't be a database or any kind of local storage on this project, so any bot configuration settings such as your selected Twitter filters won't persist between Bot sessions.

 - Adapt the code that you wrote for the Slack client, to publish tweets coming from the Twitter client.
 - You'll need to create a command parser for your integration-- something to instruct SlackTweet about which twitter users, keywords or hashtags to subscribe to.
 - Implement a full CRUD (Create, Read, Update, Delete) interface for twitter subscriptions:
   - Be able to list all current subscriptions
   - Add and delete subscriptions
   - Control the slack channel(s) where incoming tweets are directed to
   - Example interface screenshot:
 <img src="img/bot_interface.png" width="471" height="211" />
  
 - Implement a Bot command that can print some statistics such as
   - Total uptime
   - Number of tweets received per minute
   - Most frequent Tweet source
   - Other Source & Traffic metrics you may think of

## Deployment Details
NOTE: This section assumes that you have already created a Heroku account from previous assignments, and you have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) tools installed on your local development machine.

During development of your Slackbot, you will be running and debugging your code from your local machine.  When things are working well, it's time to try out a cloud deployment.

Most of the python Heroku deployment examples on the internet assume that you are developing a web app, but in this case you are deploying a simple standalone python script without a framework or WSGI gateway.  In order to deploy your bot to Heroku, your github repo must contain some special files named `Procfile` and `runtime.txt`.  `Procfile` tells Heroku which program to run when you activate your free dyno instance.  Your Procfile should contain a single line like this:
```
worker: python slacktweet.py
```
`Runtime.txt` tells Heroku which python interpreter version to use when it constructs a docker image for your slackbot.  You should select a version that matches the one that you used while developing in your virtual environment.  See which python versions are supported by Heroku [here](https://devcenter.heroku.com/articles/python-support).  Sample contents of `runtime.txt`:
```
python-3.7.5
```
Your slacktweet application is designed to be long-running, so it seems natural to try and deploy it on a cloud hosting platform such as Heroku.  However, Heroku limits the free-tier cloud hosting 'dynos' to a maximum uptime of 18 hours per 24-hour period.  So your bot will be forcibly euthanized with a SIGTERM every so often (unless you upgrade to Hobby tier -- $7.00/month). 

```
heroku create slacktweet
git push heroku master
```
Remember that your `.env` file should contain your slack and twitter API tokens, and it **should not be part of your repo** (that is, .env should be listed in your .gitignore).  You will need to copy your API tokens directly into Heroku config vars:

```
heroku config:set BOT_USER_TOKEN="xoxb-431941958864-124971466353-2Ysn7vyHOUkzjcABC76Tafrq"
heroku config:set OTHER_TOKEN="other-value"
```
Now everything should be ready to run.  Start up your slacktweet app and check the logs.  Find out more about viewing heroku logs [here](https://devcenter.heroku.com/articles/logging)

```
heroku ps:scale worker=1
heroku logs --tail
``` 

## Guidance Notes
You will submit a link to a github repository that you create and curate on your own instead of forking from this Kenzie repo.  Remember that your work on github will become your own personal portfolio that you will want to show off to recruiters and potential employers.   With that said, here are a few best-practices that we will be looking for in your repo:

## Source Code Best Practices
- PEP8: No warnings
- Docstrings and #comments for functions and modules
- Non-monolithic, modular structure (short, concise functions) that adhere to the single-responsibility principle
- Well-named variables, classes, and functions
- Readability, maintainability

## Development Best Practices
 - Collaborate with your Teammate. Research and plan .. Use VSCode Liveshare for pairing sessions
 - Create and use a project virtual environment with pipenv.  DO NOT commit your virtual environment to your repo!
 - pipenv install any new packages into your virtualenv
 - Configure your IDE to use the interpreter from your virtual environment
 - Use your IDE and debugger to run, step, and view
 - Keep your API tokens in a separate `.env` file and don't push them to the repo! Use a package such as [`python-dotenv`](https://pypi.org/project/python-dotenv/) to load your tokens.
 - Use python logging (not print statements) for all output messages. See additional notes about logging below.

## Repo Best Practices
 - Have a descriptive top-level README.md (like this one!).  If you don't know what a good README looks like, google "README best practices"
 - `.gitignore` is present, ignorning `.vscode/` and `.env` and `.log` and `venv/`
 - `requirements.txt` from pip freeze
 - No hard-coded API keys or tokens anywhere.  __DO NOT LEAK TOKENS__.
 - Small, incremental commits with meaningful messages-- not "blah foo bar" or "asdfadfadfadfadfasdfasdf"
 - Don't commit log files or virtual envs to the repo.
 

**Notes on Logging** -- Your Slacktweet app should log to both the console and a rotating log file.  Low-frequency events should be logged at INFO level, and high-frequency at DEBUG.
 Exception handlers should log at ERROR or above for anything unhandled. Other levels are self-explanatory.  Use an environment variable to select logging output level when your Bot starts.  Log startup and shutdown events, as well as slack/tweepy client connection info and any disconnect events.  Log every command message that your Bot receives and sends to the Slack or Twitter API.  Manage your file logging with some kind of time rotation or deleting schedule so that logs do not grow unbounded.  The Python logging module has built-in ways to do this.

**OS Signal Handling** -- The Slackclient 2.x Python library now supports built-in OS Signal handling of SIGTERM and SIGINT.  So you do not need to explicitly install a signal handler into your bot.  However, you still need to gracefull shut down your instances of SlackClient and TwitterClient when this signal is received.  In a free-dyno Heroku deployment, your program WILL receive a SIGTERM at least once per day, when it wants your Bot to go to sleep.  Take that opportunity to gracefully close any open connections to Slack or Twitter and log a shutdown banner.

**Exception Handling** -- Bot should not ever exit unless it is requested (either by user command or OS signal).  Your Bot should handle exceptions in order from most detailed (narrow, specific) to most broad.  Unhandled exceptions (the ones without specific handlers) should log full stack traces.  Strive for high availability by running your Bot in a local test environment for as long as you can.  We have a linux desktop server on site for this-- ask your instructor for account access. Harden against wifi outages and whimsical disconnections of your slack and twitter clients by inserting exception handlers for specific cases you encounter.  When you catch an unhandled exception, pause for a few additional seconds before restarting your loop.  Don't spam the logs with a ton of "Restarting ..." messages-- allow a few moments for the OS process manager to send your Bot a SIGINT or SIGTERM if the process monitor thinks that Bot is misbehaving.  You can test your exception handler by adding a special bot command of your own design, that will manually raise any exception from within your program.   Hint:  this uses the `raise` Python function ..
 
## Demos
For your grade on this project, your team must demonstrate all items in the rubric to the instructor/facilitator team.  

## Final Words
This assignment brings together many concepts that you have learned in the preceding months.  While it is not an SE capstone project, it does have significant point value and we encourage your team to get started early.  

# Good Luck!!
