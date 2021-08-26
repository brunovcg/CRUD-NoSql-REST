from flask import Flask,jsonify, request
from app.controllers.def_controllers import (add_post, del_post, get_many_posts, get_one_post, upd_post, check_request)
from datetime import datetime


def home_view(app: Flask):

    @app.post("/posts")
    def create_post():

        try:
            title = request.get_json()["title"]
        except KeyError:
            title = None

        try:
            author = request.get_json()["author"]
        except KeyError:
            author = None

        try:
            tags = request.get_json()["tags"]
        except KeyError:
            tags = None

        try:  
            content = request.get_json()["content"]
        except KeyError:
            content = None

        anwser_message = add_post(title, author, tags, content)
        test_request_for_wrong_or_missing = check_request("create", anwser_message)

        if test_request_for_wrong_or_missing:
            return test_request_for_wrong_or_missing, 400
                
        anwser_message.pop("_id")

        return jsonify(anwser_message), 201


    @app.delete("/posts/<int:id>")
    def delete_post(id: int):
        is_deleted = del_post(id)

        if not is_deleted:
            return {"error" : f"There is no ID '{id}' in post database"}, 404

        return is_deleted, 200
        

    @app.get("/posts/<int:id>")
    def read_post_by_id(id:int):
        post = get_one_post(id)

        if post == "Not found":
            return {"Error" : f" ID '{id}' was not found on your database"}, 404

        return post, 200


    @app.get("/posts")
    def read_posts():
        all_posts = get_many_posts()

        if all_posts == []:
            return {"Error" : "Our database is Empty"},404
        
        return jsonify(all_posts), 200


    @app.patch("/posts/<int:id>")
    def update_post(id : int):
        itens_to_update = request.get_json()

        test_request_for_wrong_or_missing = check_request("update", itens_to_update)

        if test_request_for_wrong_or_missing:
            return test_request_for_wrong_or_missing, 400
          
        time_now = datetime.utcnow()
        itens_to_update["updated_at"] = time_now
        is_updated = upd_post(id , itens_to_update)

        if not is_updated:
            return {"error" : f"There is no ID '{id}' in post database"}, 404

        return is_updated, 200
        

    @app.get("/")
    def home():
        return {"message":"Welcome to Exercise 9 - CRUD NoSQL APP Q3"}, 200
   