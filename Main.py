import os
import prototype_mediapipe
import realtime_continues_speech

class RealTimeFlowChart:

    def __init__(self) -> None:
        self.PATH_self_dir = os.path.dirname(os.path.realpath(__file__))

        self.OBJ_mediapipe = prototype_mediapipe.MediaPipeDemo()
        self.OBJ_arts = realtime_continues_speech.SpeechRecognizer()



if __name__ == "__main__":
    OBJ_RTFC = RealTimeFlowChart()