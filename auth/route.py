from fastapi import APIRouter, Form, Request, Response, HTTPException, Depends
from extensions.password_hasher import verify_password
from account.models import User
from auth.session import create_session_token, get_user_from_request

router = APIRouter()

# -------------------------
# Login
# -------------------------
@router.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    user = User.filter(username=username).first()
    if not user:
        raise HTTPException(status_code=403, detail="user does not exists")
    print("drrr",user)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # make token session
    token = create_session_token(user.id)

    # send cookie to HttpOnly
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        max_age=60*60*24,  # 1 day
        samesite="lax"
    )
    return {"message": "Logged in successfully"}

# -------------------------
# Logout
# -------------------------
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out successfully"}

# -------------------------
# Get current user
# -------------------------
@router.get("/me")
async def get_current_user(request: Request):
    user_id = get_user_from_request(request)
    user = User.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "image": user.image,
        "is_superuser": user.is_superuser
    }
