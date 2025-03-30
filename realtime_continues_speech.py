import azure.cognitiveservices.speech as speechsdk
import re
import requests


class SpeechRecognizer:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(subscription="SUBSCRIPTION_KEY", region="region")
        self.speech_config.speech_recognition_language = "en-US"
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)
        self.buffer = ""
        self.target_phrases = ["make it a circle",
                                "make it a rectangle",
                                "change color to ",
                                "add text ",
                                "place the graphic"]

    def start_recognition(self):
        self.speech_recognizer.recognized.connect(self.recognized_callback)
        self.speech_recognizer.start_continuous_recognition_async()
        print("Listening...")

    def stop_recognition(self):
        self.speech_recognizer.stop_continuous_recognition()

    def recognized_callback(self, evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(evt.result.text))
            self.buffer += " " + evt.result.text
            self.buffer = self.buffer.strip()
            self.check_for_phrase()

    def check_for_phrase(self):
        for phrase in self.target_phrases:
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            if pattern.search(self.buffer):
                print("Phrase detected: {}".format(phrase))
                self.phrase_detected = True
                self.handle_detected_phrase(phrase)
                self.buffer = ""
                break
            else:
                self.phrase_detected = False

    def handle_detected_phrase(self, phrase):
        attr_dict = {}

        if "make it a circle" in phrase.lower():
            attr_dict["name"] = "circle"
        elif "make it a rectangle" in phrase.lower():
            attr_dict["name"] = "rectangle"
        elif "change color to " in phrase.lower():
            color_match = re.search(r"change color to (\w+)", self.buffer, re.IGNORECASE)
            if color_match:
                color = color_match.group(1)
                attr_dict["color"] = color.lower()
                print("Color detected: {}".format(color.lower()))  # Debugging line
            else:
                print("No color detected")  # Debugging line
        elif "add text " in phrase.lower():
            text_match = re.search(r"add text (.+)", self.buffer, re.IGNORECASE)
            if text_match:
                text = text_match.group(1).strip()
                attr_dict["text"] = text
                print("Text detected: {}".format(text))  # Debugging line
            else:
                print("No text detected")  # Debugging line
        elif "place the graphic" in phrase.lower():
            attr_dict["place"] = True

        self.call_change_attribute_api(attr_dict)

    def call_change_attribute_api(self, attr_dict):
        print(attr_dict)
        url = f"http://localhost:8000/change_attribute/"
        try:
            response = requests.get(url, params=attr_dict)
            if response.status_code == 200:
                print("Attribute changed successfully")
            else:
                print("Failed to change attribute")
        except Exception as e:
            print("Error making API call:", e)


if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    try:
        target=recognizer.start_recognition()
        input("Press Enter to stop...\n")
    finally:
        recognizer.stop_recognition()
