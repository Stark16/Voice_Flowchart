from fastapi import FastAPI
import cv2
import asyncio

app = FastAPI()

cap = cv2.VideoCapture(0)

@app.on_event('startup')
async def startup_event():
    asyncio.create_task(read_feed())

async def read_feed():
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        await asyncio.sleep(0.01)