import speech_recognition as sr
import threading

import spacy
import json

def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
        return ("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return("Could not request results from Google Speech Recognition service; {0}".format(e))
        

def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source)
        return audio



def extract_keywords_from_text(input_text):
    nlp = spacy.load("en_core_web_md")
    doc = nlp(input_text)

    common_words = ["a", "an", "the", "of", "is", "are", "what", "give", "me", ","]

    keywords = []

    # Track if the previous token should be combined with the current token
    combine_tokens = False
    combined_token = ""

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and token.text.lower() not in common_words:
            if combine_tokens:
                # If the previous token should be combined, append it to the combined token
                combined_token += "_" + token.text
            else:
                # Otherwise, add the current token as a keyword
                keywords.append(token.text)

            # Check if the next token should be combined
            if token.dep_ == "compound":
                combine_tokens = True
            else:
                combine_tokens = False
    print(keywords)
    return keywords


def extract_keywords_from_file(input_file_path):
    # Read the contents of the input file
    with open(input_file_path, 'r') as file:
        input_text = file.read()

    # Extract keywords from the input text
    keywords = extract_keywords_from_text(input_text)

    return keywords



if __name__ == "__main__":
    audio = capture_audio()
    transcribe_result = transcribe_audio(audio)

    # Save the transcribe_result to a file
    with open('Vedant Try/output.txt', 'w') as file:
        file.write(str(transcribe_result))

    input_file_path = 'Vedant Try/output.txt'

    keywords = extract_keywords_from_file(input_file_path)

    # combined_query = " ".join(keywords)

    with open('Vedant Try/entity.txt', 'w') as file:
        combined_keywords = "_".join(keywords)
        file.write(str(combined_keywords))


