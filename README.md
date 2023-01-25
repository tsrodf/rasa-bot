# rasa-bot

## Table of Content

- [Concepts](#concepts)
- [Why intent-based chatbots](#why-intent-based-chatbots)
- [Examples for intent-base chatbots](#examples-for-intent-based-chatbots)
- [Discarded Concepts](#discarded-concepts)
- [Technologies used](#technologies-used)
- [Installation](#installation)
  - [Interact through Shell](#interact-through-shell)
  - [Interact with REST-Service](#interact-with-rest-service)
  - [Interact with Websocket](#interact-with-websocket)
  - [Advanced remote server setup](#advanced-remote-server-setup)
- [Add new intents and responses](#add-new-intents-and-responses)
  - [Observations](#observations)
- [Actions added](#actions-added)
  - [Tests *action_get_weather*](#tests-action_get_weather)
- [Reminder event (Disabled)](#reminder-event-disabled)
- [Rasa commands](#rasa-commands)



### Concepts:

NLP(Natural Language Processing) helps interact in a human-like way.

We don’t have to match predefined questions character by character. Also it feels more natural for users to write like they would with a human instead of pressing buttons or using forms.

### Why intent-based chatbots?

- They don’t have to follow a specific conversational path. They can adapt to an user changing their mind
- Good at answering specific predefined question-patterns

#### Examples for intent-based chatbots:

- Dialogflow1 (originally named Api.ai), developed by Google
- wit.Ai developed by Facebook are used in academic research (Handoyo et al., 2018; Rosruen & Samanchuen, 2019)

### Discarded Concepts:

- [Custom intent-based chatbot with pytorch and nltk built from scratch](https://github.com/Blankjr/my-nlp-chatbot).

-  **Benefits:**
    - Lightweight process
    - fast training process

  - **Drawback:**
     - Only single question/answer conversions possible in our prototype
     - Extracting variables from question not possible

### Technologies used:

- Rasa

  - with over 25 million downloads, Rasa Open Source is the most popular open source framework for building chat and voice-based AI assistants.

  - **Benefits:**

    - Open Source Version available
    - Self Host-able
    - Building REST-/ Websocket-Channel
    - Third party system connectors
    - [Stories](https://rasa.com/docs/rasa/stories/) (conversation paths) https://rasa.com/docs/rasa/writing-stories/ 

  - **Drawback:**

     - Relative resource intense
     - Long cold start time
     - Training pipeline takes a while.
     - Documentation is lacking

- Linux

  - The rasa chatbot is hosted on a VM with a headless linux distro.

- Ngrok

  - Ssh tunnel for public https connectivity of the local rasa process

## Installation

1. Create environment with conda: `conda create --name <name> python=3.8`
2. Activate environment with conda: `conda activate <name>`
3. Install rasa: `pip install rasa`
4. Create folder *rasa* and cd into it: `mkdir rasa`
5. Create new project: `rasa init`

### Interact through shell

1. Activate the environment in which rasa was installed if needed.
2. Run conversation through shell: `rasa shell`
3. To stop shell: `/stop`

### Interact with REST-Service:

1. Start server with (only) REST interface: `rasa run --connector rest` ( bind specific local ip: `-i  192.168.50.150`)
2. Start action server: `rasa run actions`
3. Interact with REST Interface: `http://0.0.0.0:5005/webhooks/rest/webhook`

- Send a POST Message to the REST Server with a JSOn Body:
  - `{ "sender": "test_user", "message": "Hi there!"}`
  - Response: `[{"recipient_id": "test_user", "text": "Hey! How are you?"}]`

### Interact with Websocket:

1. Start server with CORS enabled: `rasa run --enable-api --cors "*"`
2. Start action server: `rasa run actions`
3. Start a webserver of your choice inside the subfolder `./webclient`

### Advanced remote server setup

Instructions found in this document:
https://github.com/tsrodf/rasa-bot/blob/main/server/server_setup.md

## Add new intents and responses

1. Extend *nlu.yml* file with new intents and interactions.
2. Add utter responses to *domain.yml* file.
3. Write `rasa train` to train the chatbot.

### Observations

1. Intents have to be also included in *domain.yml*.
2. Rasa chooses a random option from responses.
3. Even if a word or sentence is included in *nlu.yml*, in order for the bot to react to it's necessary to write a story to *stories.yml*.
4. Don't forget to write `rasa run actions` to call custom actions!

## Actions added

- action_get_weather
- action_get_joke
- action_get_activity

### Tests *action_get_weather*

1. Default location is Dusseldorf

```
# default loc: Dusseldorf
loc = 'Dusseldorf'
```

1. Test: tracker.latest_message.get("entities")

```
# test 1 -> tracker.latest_message.get("entities")
# it only works when 
# - the given location is saved as intent weather_for_location into nlu.yml
# - location is defined as entity in domain.yml
entities = tracker.latest_message.get("entities")
if entities:
loc = entities[0]["value"]
# end test 1
```

1. Test: tracker.latest_message.get("text")

```
# test 2 -> tracker.latest_message.get("text")
# it works but the location should be at a certain position
# if not the location won't be recognized
text = tracker.latest_message.get("text")
words = text.split()
#s = text.find("weather")
ind = words.index("weather")
if len(words) > ind+2 and (words[ind+1] == 'in' or words[ind+1] == 'of'):
loc = words[ind+2]
# end test 2
```

1. Test if it shows location

```
dispatcher.utter_message(loc)
return []
```

## Reminder event (Disabled)

- Added reminder event and done some tests (https://github.com/RasaHQ/rasa/blob/main/examples/reminderbot)
- Reminders can be included in some actions to trigger a specific bot response at a given time.
  - it can simulate that the bot has taken the lead to change the subject or to talk about something in particular (e.g. ask what have you done yesterday)
  - Disabled for chattingchatbots moderator compatibility

### Rasa commands

| Command      | Effect                                                       |
| ------------ | ------------------------------------------------------------ |
| `rasa init`  | Creates a new project with example training data, actions, and config files |
| `rasa shell` | Loads your trained model and lets you talk to your assistant on the command line. |
| `rasa train` | Trains a model using your NLU data and stories, saves trained model in `./models.` |

