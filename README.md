# rasa-bot

## Installation

1. Create environment with conda: `conda create --name rasabot python=3.8` 
2. Activate environment with conda: `conda activate rasabot`
3. Install rasa: `pip install rasa`
4. Create folder *rasa* and cd into it: `mkdir rasa`
5. Create new project: `rasa init` 

> Note: Rasa is installed through Conda, which was installed at `C:\Users\tsrod\anaconda3`, but the project is generated at the indicated location `C:\Users\tsrod\Documents\github\rasa-bot\rasa`.

## How to use it

1. Activate environment with conda: `conda activate rasabot`
2. Run conversation through shell: `rasa shell`
3. Stop shell: `/stop`
4. Deactivate environment: `conda deactivate`

### Interact via REST Service:
1. Start server with (only) REST interface: `rasa run --connector rest` ( bind specific local ip: `-i  192.168.50.150`)
2. Start action server: `rasa run actions`
3. Interact with REST Interface: `http://0.0.0.0:5005/webhooks/rest/webhook`
- Send a POST Message to the REST Server with a JSOn Body:
  - `{ "sender": "test_user", "message": "Hi there!"}`
  - Response: `[{"recipient_id": "test_user", "text": "Hey! How are you?"}]`
### Interact via Websocket:
1. Start server with CORS enabled: `rasa run --enable-api --cors "*"`
2. Start action server: `rasa run actions`
3. Start a webserver of your choice inside the subfolder `./webclient`
## Add new intents and responses

1. Extend *nlu.yml* file with new intents and interactions.
2. Add utter responses to *domain.yml* file.
3. Write `rasa train` to train the chatbot.

### Observations

1. Intents have to be also included in *domain.yml*.
2. Rasa chooses a random option from responses.
3. Even if a word or sentence is included in *nlu.yml*, in order for the bot to react to it's necessary to write a story to *stories.yml*.
4. Don't forget to write `rasa run actions` to call custom actions!

## Try to add *weather* example
https://www.geeksforgeeks.org/chatbots-using-python-and-rasa/ 
- Follow steps
- `rasa shell nlu` doesn't show the right info
- Test failed
  - Link to API doesn't seem to work anymore
  - API not free / with limited use ?

## Actions added
- action_get_weather
- action_get_joke
- action_get_activity

### Tests _action_get_weather_
1. Default location is Dusseldorf
```python
# default loc: Dusseldorf
loc = 'Dusseldorf'
```
2. Test: tracker.latest_message.get("entities")
```python
# test 1 -> tracker.latest_message.get("entities")
# it only works when 
# - the given location is saved as intent weather_for_location into nlu.yml
# - location is defined as entity in domain.yml
entities = tracker.latest_message.get("entities")
if entities:
loc = entities[0]["value"]
# end test 1
```
3. Test: tracker.latest_message.get("text")
```python
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
4. Test if it shows location
```python
dispatcher.utter_message(loc)
return []
```

## Reminder event
- Added reminder event and done some tests (https://github.com/RasaHQ/rasa/blob/main/examples/reminderbot)
- Reminders can be included in some actions to trigger a specific bot response at a given time. 
  - it can simulate that the bot has taken the lead to change the subject or to talk about something in particular
  (e.g. ask what have you done yesterday)

### Some public APIs
https://github.com/public-apis/public-apis

### Rasa commands

| Command | Effect |
|---------|--------|
| `rasa init` | Creates a new project with example training data, actions, and config files |
| `rasa shell` | Loads your trained model and lets you talk to your assistant on the command line. |
| `rasa train` | 	Trains a model using your NLU data and stories, saves trained model in `./models.` |
