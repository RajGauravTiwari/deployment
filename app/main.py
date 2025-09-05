from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import cloudinary.uploader
import uuid
import random
from io import BytesIO
from app import utils
from app.mongodb import collection

# Cloudinary config
import cloudinary
cloudinary.config(
    cloud_name="dyicnb8vr",
    api_key="419838291771888",
    api_secret="IkRx_Ak939_AkhdFBuSSbh72rfE"
)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Helpers ----------
def fix_mongo_ids(doc):
    """Convert ObjectId to string for FastAPI JSON response"""
    doc["_id"] = str(doc["_id"])
    return doc

# ---------- Routes ----------
@app.post("/upload/")
async def upload_cv(
    job_role: str = Form(...),
    job_description: str = Form(...),
    uploader_email: str = Form(...),
    file: UploadFile = File(...)
):
    # Save file content to memory
    contents = await file.read()

    # Upload to Cloudinary
    result = cloudinary.uploader.upload(
        contents, resource_type="auto"
    )
    file_url = result.get("secure_url")

    # Reset file content for text extraction
    file_stream = BytesIO(contents)

    # Extract text from CV file
    cv_text = await utils.extract_text_from_bytes(file_stream, file.filename)

    # Generate dummy score + feedback
    score = random.randint(50, 100)
    feedback = "Auto-generated feedback: candidate has relevant skills but needs improvement."

    record = {
        "id": str(uuid.uuid4()),
        "job_role": job_role,
        "job_description": job_description,
        "uploader_email": uploader_email,
        "file_url": file_url,
        "file_name": file.filename,
        "score": score,
        "feedback": feedback,
        "cv_text": cv_text,
    }

    result = await collection.insert_one(record)
    record["_id"] = str(result.inserted_id)  # ✅ fix ObjectId issue

    return {"message": "Uploaded successfully", "data": record}


@app.get("/job_roles/")
async def get_job_roles():
    roles = await collection.distinct("job_role")
    return roles


@app.get("/uploads/")
async def get_all_uploads():
    docs = await collection.find().to_list(length=100)
    return [fix_mongo_ids(doc) for doc in docs]


@app.get("/scores/")
async def get_scores(job_role: str):
    docs = await collection.find({"job_role": job_role}).to_list(length=100)
    return [fix_mongo_ids(doc) for doc in docs]
