from config.settings import app

from account.route import router as UserRouter
from auth.route import router as AuthRouter
from post.route import router as PostRouter
from post.category_route import router as CategoryRouter

app.include_router(UserRouter, prefix="/account", tags=['Account'])
app.include_router(AuthRouter, prefix="/auth", tags=['Auth'])
app.include_router(PostRouter, prefix="/post", tags=['Post'])
app.include_router(CategoryRouter, prefix="", tags=['Category'])