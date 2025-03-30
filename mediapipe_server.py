import cv2
import mediapipe as mp
import asyncio
from fastapi import FastAPI
from typing import Optional
import os

app = FastAPI()

class MediaPipeDemo:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5, init_with_fast_api=False):

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(model_complexity=0, min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)

        self.shapes = ["rectangle", "circle", "rhombus"]
        self.colors_options = {
                                "red": (0, 0, 255),
                                "green": (0, 255, 0),
                                "blue": (255, 0, 0),
                                "yellow": (0, 255, 255),
                                "cyan": (255, 255, 0),
                                "magenta": (255, 0, 255),
                                "white": (255, 255, 255),
                                "black": (0, 0, 0),
                                "orange": (0, 165, 255),
                                "purple": (128, 0, 128)
                                }
        
        self.current_shape = {"name" : "rectangle", "text" : "Text Here", "loc" : None, "color" : self.colors_options["blue"]}
        self.all_shapes = [self.current_shape]


    def change_shape_dictibute(self, name=None, color=None, place=False, text=None):

        if (place):
            self.all_shapes.append(self.current_shape)
            self.current_shape = {"name" : "rectangle", "text" : "Text Here", "loc" : None, "color" : self.colors_options["blue"]}

        if name!=None :
            self.current_shape["name"] = name 
        if color != None:
            self.current_shape["color"] = self.colors_options[color]
        if text != None:
            self.current_shape["text"] = text
        print(self.current_shape)


    def calc_finger_locs(self, image, landmarks):

        index_finger_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        h, w, _ = image.shape
        x1, y1 = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
        x2, y2 = int(thumb_tip.x * w), int(thumb_tip.y * h)

        self.current_shape["loc"] = ((x1, y1), (x2, y2))
        self.all_shapes[-1] = self.current_shape

        self.draw_shapes(image)


    def draw_shapes(self, image):
        shape_line = []
        for shape_dict in self.all_shapes:

            text = shape_dict['text']
            color = shape_dict['color']

            (x1, y1), (x2, y2) = shape_dict["loc"]
            if shape_dict["name"] == self.shapes[0]:

                cv2.rectangle(image, (x1, y1), (x2, y2), color, -1)
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

                if (len(shape_line) == 0):
                    curr_point = (x2, y1 + (abs(y2 - y1)//2))
                    shape_line = [curr_point]

                elif (len(shape_line) == 1):
                    curr_point = (x1, y1 + (abs(y2 - y1)//2))
                    shape_line.append([curr_point, (x2, y1 + (abs(y2 - y1)//2))])

                else:
                    curr_point = (x1, y1 + (abs(y2 - y1)//2))
                    shape_line[0] = shape_line[1][1]
                    shape_line[1] = [curr_point, (x2, y1 + (abs(y2 - y1)//2))]

            if  shape_dict["name"] == self.shapes[1]:

                x, y = (x1 + x2) // 2, (y1 + y2) // 2
                radius = int(pow( pow(x1 - x, 2) + pow(y1 - y, 2), 1/2))
                curr_point = (x + radius, y)

                if (len(shape_line) == 0):
                    curr_point = (x + radius, y)
                    shape_line = [curr_point]

                elif (len(shape_line) == 1):
                    curr_point = (x - radius, y)
                    shape_line.append([curr_point, (x + radius, y)])

                else:
                    curr_point = (x - radius, y)
                    shape_line[0] = shape_line[1][1]
                    shape_line[1] = [curr_point, (x + radius, y)]

                cv2.circle(image, (x, y), radius=radius, color=color, thickness=-1)

                center_x, center_y = (x, y)
                box_size = pow(2, 1/2)*radius
                (x1, y1), (x2, y2) = (x - 0.5*box_size, y - 0.5*box_size), (x + 0.5*box_size, y + 0.5*box_size)
            
            print(self.all_shapes)
            font_scale = min(abs(x2 - x1), abs(y2 - y1)) / 150.0
            font_scale = max(font_scale, 0.1)
            font_thickness = int(font_scale * 2)

            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            text_x, text_y = center_x - text_width // 2, center_y + text_height // 2

            cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)


            if len(shape_line) == 2:

                prev_point = shape_line[0]
                if len(shape_line[1]) == 1:
                    new_point = shape_line[1]
                elif len(shape_line[1]) == 2:
                    new_point = shape_line[1][0]

                cv2.line(image, prev_point, new_point, color=(0, 0, 0))
                cv2.circle(image, new_point, 3, (255, 255, 255))
                cv2.circle(image, prev_point, 3, (255, 255, 255))



    def process_single_frame(self, image):

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.hands.process(image)

        image.flags.writeable = True
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image_bgr,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )

                self.calc_finger_locs(image_bgr, hand_landmarks)

        return image_bgr



hand_gesture_recognition = MediaPipeDemo()

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(main())

async def main():

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, image = cap.read()
        
        if not ret:
            continue
        processed_image = hand_gesture_recognition.process_single_frame(image)
        cv2.imshow('Hand_rectangles', processed_image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
        await asyncio.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()
    os._exit(-1)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/change_attribute/")
def change_attr(
    name: Optional[str] = None, 
    color: Optional[str] = None, 
    place: Optional[bool] = False, 
    text: Optional[str] = None
):

    hand_gesture_recognition.change_shape_dictibute(name, color, place, text)