from config.settings import app

from account.route import router as UserRouter
from auth.route import router as AuthRouter
from post.route import router as PostRouter

app.include_router(UserRouter, prefix="/account", tags=['Account'])
app.include_router(AuthRouter, prefix="/auth", tags=['Auth'])
app.include_router(PostRouter, prefix="/post", tags=['Post'])