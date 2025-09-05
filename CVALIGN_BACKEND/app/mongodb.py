# app/mongodb.py






from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://rajt4656:Raj%40mongo@clusterraj.xvhsrzx.mongodb.net/?retryWrites=true&w=majority&appName=ClusterRaj"
)

client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True  # Windows SSL fix
)

db = client["cvalign"]
collection = db["cvs"]
