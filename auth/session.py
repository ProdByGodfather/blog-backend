from itsdangerous import URLSafeTimedSerializer
from fastapi import Request, HTTPException
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
SESSION_EXPIRE_SECONDS = 60 * 60 * 24  # 1 روز

serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_session_token(user_id: int) -> str:
    return serializer.dumps(user_id)

def verify_session_token(token: str) -> int:
    try:
        user_id = serializer.loads(token, max_age=SESSION_EXPIRE_SECONDS)
        return int(user_id)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

def get_user_from_request(request: Request):
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return verify_session_token(token)
