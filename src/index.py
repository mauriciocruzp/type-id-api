from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from keras.models import load_model

app = FastAPI()

classes = [
    "sans-serif",
    "serif",
    "impact",
    "times-new-roman",
    "comic-sans",
    "anton",
    "pacifico",
    "creepster",
    "bangers",
    "monoton",
]

model = load_model("src/models/model.h5")


@app.post("/type")
async def upload_image(image: UploadFile = File(...)):
    image_bytes = await image.read()

    image_np = np.frombuffer(image_bytes, np.uint8)

    image_gray = cv2.imdecode(image_np, cv2.IMREAD_GRAYSCALE)

    image = cv2.resize(image_gray, (64, 64))

    image = np.array(image).reshape(-1, 64, 64, 1)

    prediction = model.predict(image)
    predicted_class = classes[np.argmax(prediction)]

    return {"class": predicted_class}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
