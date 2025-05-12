import json
from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print(f'Session path: {session}\n')

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={
                'session': session,
                'query_input': query_input
            }
        )

        print("=" * 50)
        print(f'''Query text: {response.query_result.query_text}
Detected intent: {response.query_result.intent.display_name} (confidence: {response.query_result.intent_detection_confidence})\n
Fulfillment text: {response.query_result.fulfillment_text}\n''')
        return response.query_result.fulfillment_text


with open('intents.json', 'r') as my_file:
    intents_json = my_file.read()
INTENTS = json.loads(intents_json)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


if __name__ == '__main__':
    detect_intent_texts('magic-fjpn', '123456789', ['Хай'], 'ru-RUS')
    for intent in INTENTS:
        create_intent('magic-fjpn', intent, INTENTS.get(intent)['questions'], [INTENTS.get(intent)['answer']])
