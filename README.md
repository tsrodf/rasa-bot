# Rasa-bot

## Table of Contents

- [Concepts](#concepts)
- [Why intent-based chatbots](#why-intent-based-chatbots)
- [Examples for intent-based chatbots](#examples-for-intent-based-chatbots)
- [Discarded Concepts](#discarded-concepts)
- [Technologies used](#technologies-used)
- [Rasa components](#rasa-components)

- [Guidelines](#guidelines)
  - [Installation with conda](#installation-with-conda)
  - [Interact through Shell](#interact-through-shell)
  - [Interact with REST-Service](#interact-with-rest-service)
  - [Interact with Websocket](#interact-with-websocket)
  - [Advanced remote server setup](#advanced-remote-server-setup)
  - [Training](#training)

## Concepts

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

## Rasa components

### Domain

The domain defines the universe where the rasa-bot performs its function. It defines the intents, the responses and a configuration for conversation sessions and it can also include entities, slots, forms and actions.

The domain consists of either one or several YAML files. When the content is split across multiple documentos it's automatically read and merge.

#### Intents

Intents are categories in which the messages received by the rasa-bot are grouped. They represent the purpose of the user interacting with the bot and are listed in the domain file (see [NLU data](#nlu-data)). It's also possible to use or ignore certain entities for an intent.

#### Responses

Responses are actions that send a message to a user without running any custom code or returning events. They can be directly defined in the domain file. In order to receive a wider range of responses it's recommended to add more than one example to each response. Rasa chooses one answer randomly.

#### Session configuration

It represents the dialogue between the bot and the user. Conversation sessions can begin when the user starts the conversation, when the user sends a message after a period of inactivity or manually triggered with an intent message. It's possible to determine the session expiration time and the option to carry over slots to a new session.

#### Entities

Entities are structured pieces of information inside a user message, which have to be extracted by either specifying them or defining regular expressions. By default, entities influence action prediction it's possible to configure the domain in order to ignore entities for certain intents. Entities roles and groups can also be defined.

#### Slots and Forms

Slots represent the bot's memory. They could be used to store information provided by the user or coming from the outside (e.g. through APIs). They should be defined with a name, a type and predefined mappings. Slots can also influence the conversation behavior. The Slot types are are text, boolean, categorical, float, list, any or custom - which should be self-defined.

Forms are a special type of action intended to help the bot collect information about the user.

#### Actions

Actions are the things that the bot can actually do. The most common examples are respond to a user, make an external API call or query a database. Responses are included in the domain file, whereas custom actions are only listed on it but they have to be implemented in the actions file.

### NLU data

The main objective of NLU (Natural Language Understanding) is to extract structured data from user messages. This information consists of the user's intent and any entities used. It's possible to define some additional information, such as Regular Expressions and Lookup Tables.

NLU data is included in a YAML file, which consists of intents and synonyms. It should contain at least two examples for each intent to facilitate recognition. The latter can be used to store words which can designate the same entity.

### Stories

Stories represent a conversation beetween a user and a bot. They have a name and steps consisting of several intents and actions. When using events, checkpoints and statements they need to be specified. They have to be written to the stories YAML file.

### Rules

Rules are used to handle small specific conversation patterns, but they cannot generalize to unseen conversation paths, unlike stories. Their overuse is not recommended and the `RulePolicy` should be included in the model configuration. They are included in the rules YAML file.

There are other components, some of which have been already mentioned, that will not be explained any further since they have not been used in this project.

### Reminders

Reminders are used to reach out to the used after a set amount of time in order. A reminder has to be scheduled and a reaction to it needs to be specified. It's also possible to define an action in order to cancel its effect.

In a previous phase of the project reminders were implemented to trigger a specific bot response at a given time to simulate that the bot had taken the lead to change the subject or talk about something in particular. This option was disabled since it does not suit the specifications of the project.

## Rasa architecture

Rasa architecture is scalable. The two main components are Natural Language Understanding (NLU) and dialogue management, respectively represented in the following diagram as _NLU Pipeline_ and _Dialogue Policies_. The first is 
responsible for handling intent classificaton, entity extraction and response retrieval; and the latter decides the next action in a conversation based on the context.

## Limitations

If no intent detected, no response.

## Possible future enhacements
- Corpus ergänzen
- webui hosten und text to speech

## Guidelines

### Installation with conda

1. Create conda environment: `conda create --name <name> python=3.8`
2. Activate environment: `conda activate <name>`
3. Install rasa: `pip install rasa`
4. Create folder *rasa* and cd into it.
5. Run `rasa init` to create a new project with example training data, actions, and config files.

### Interact through shell

1. Activate the environment in which rasa has been installed.
2. Run `rasa shell` to load the trained model and interact with the bot on the command line.
3. Run to stop shell: `/stop`

### Interact with REST-Service

1. Start server with (only) REST interface: `rasa run --connector rest` ( bind specific local ip: `-i  192.168.50.150`)
2. Start action server: `rasa run actions`
3. Interact with REST Interface: `http://0.0.0.0:5005/webhooks/rest/webhook`

- Send a POST Message to the REST Server with a JSOn Body:
  - `{ "sender": "test_user", "message": "Hi there!"}`
  - Response: `[{"recipient_id": "test_user", "text": "Hey! How are you?"}]`

### Interact with Websocket

1. Start server with CORS enabled: `rasa run --enable-api --cors "*"`
2. Start action server: `rasa run actions`
3. Start a webserver of your choice inside the subfolder `./webclient`

### Advanced remote server setup

Instructions found in this document:
https://github.com/tsrodf/rasa-bot/blob/main/server/server_setup.md

### Training

- Run `rasa train` to train a model using provided NLU data and stories. Models are saved to `./models.`. This should be done every time the NLU data is modified.

## Sources

- Luo
- https://rasa.com/docs/rasa/ 