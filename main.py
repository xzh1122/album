from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import os
import shutil
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
from translate import Translator
import re
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    name = f"{timestamp}_{file.filename}"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # 保存后直接用文件路径进行图片分类
    try:
        tag = classify_content(file_path)
    except Exception as e:
        os.remove(file_path)
        raise e
    new_name = f"{timestamp}_{tag}_{file.filename}"
    new_path = os.path.join(UPLOAD_FOLDER, new_name)
    os.rename(file_path, new_path)
    return {"message": "File uploaded successfully", "filename": name}


@app.get("/review_photos")
async def get_uploaded_photos():
    photos = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename == '.DS_Store':
            continue
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            # 解析时间戳
            try:
                timestamp_str = filename.split('_')[0]
                tag = filename.split('_')[1]
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
                date_str = timestamp.strftime("%Y%m%d")
            except Exception:
                continue
            photos.append({
                "filename": filename,
                "tags": [tag] if tag else [],
                "timestamp": timestamp,
                "date": date_str
            })
    return photos

def classify_content(file_path: str) -> List[str]:
    image = Image.open(file_path)
    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    classify = model.config.id2label[predicted_class_idx]
    if re.search("cat", classify, re.I):
        classify = "Cat"
    tag = Translator(from_lang="english",to_lang="chinese").translate(classify)
    # try:
    #     tag = Translator(from_lang="english",to_lang="chinese").translate(classify)
    # except Exception as e:
    #     print(e)
    #     tag = classify
    return tag


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
