from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "author": "John Doe",
        "title": "Fast api is cool",
        "content": "First time trying out fastapi",
        "date_posted": "January 02, 2026",
    },
    {
        "id": 2,
        "author": "shakakibara chan",
        "title": "Nah python is gonna rule fs",
        "content": "Python have such a good syntactic beauty dawg",
        "date_posted": "January 02, 2026",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@app.get("/post/{post_id}")
def get_post_html(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"]
            return templates.TemplateResponse(
                request, "post.html", {"post": post, "title": title}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts")
def get_posts():
    return posts
