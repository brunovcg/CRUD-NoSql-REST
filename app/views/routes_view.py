from flask import Flask


def home_view(app: Flask):

    @app.post("/posts")
    def create_post():
        return "aqui para create_post"


    @app.delete("/posts/<int:id>")
    def delete_post(id):
        return "aqui para delete_post"


    @app.get("/posts/<int:id>")
    def read_post_by_id(id):
        return f"{id}"


    @app.get("/posts")
    def read_posts():
        return "aqui para read_post"


    @app.patch("/posts/<int:id>")
    def update_post(id):
        return "update_post"


    @app.get("/")
    def home():
        return "Welcome to Exercise 9 - CRUD NoSQL APP Q3"


    