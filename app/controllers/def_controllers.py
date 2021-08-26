import pymongo
from app.models.post_model import Post


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["kenzie"]


def list_posts():
    """List all posts
   
    Returns:
        list: Returns a list with all posts info 
    """
    post_list = list(db.posts.find())

    if post_list != []:

        for post in post_list:
           post.pop("_id")

    return post_list


def id_generator():
    """Generate a unique ID based on the highest ID on Mongo Database
   
    Returns:
        int: Returns the ID 
    """
    post_list = list_posts()

    if len(post_list) < 1:
        my_id = 1
    else:
        my_id = max([item["id"] for item in post_list])+1

    return my_id

def check_request(create_or_update, request_data):
    """Function to check if there are any wrong or missing data on client request
    Args: 
        create_or_update(str): set 'create' for POST and 'updade' for PATCH.
        request_data(dict): a dict with all the client request data
    Returns:
        list: if something is wrong or missing.
        boolean: False if everythong is right on function
    """
    data_type = {
        str: "string",
        int: "integer",
        float: "float",
        list: "list",
        dict: "dictionary",
        bool: "boolean",
    }
    expected_type = {
        "title" : str,
        "author" : str,
        "tags" : list,
        "content" : str,
    }
    wrong_fields = {"wrong_fields" : []}
    missing_fields = {"missing_fields" : []}
    request_needs = ["title", "author", "tags", "content"]
    request_keys_needs = dict.keys(request_data)

    if create_or_update == "create":

        for need in request_needs:
            if not request_data[need]:
                missing_fields["missing_fields"].append(need)
        
        if len(missing_fields["missing_fields"]) > 0:
            return missing_fields

        for need in request_needs:
            if type(request_data[need]) != expected_type[need]:
                wrong_fields["wrong_fields"].append({f'<{need}> should be:' : data_type[expected_type[need]]})

            if len(wrong_fields["wrong_fields"]) > 0:
                return wrong_fields
        

    if create_or_update == "update":
    
        for need in request_keys_needs:
            if type(request_data[need]) != expected_type[need]:
                wrong_fields["wrong_fields"].append({f'<{need}> should be:' : data_type[expected_type[need]]})

            if len(wrong_fields["wrong_fields"]) > 0:
                return wrong_fields     

    return False


def get_one_post(id:int):

    post = db.posts.find_one({"id":id})

    if not post:
        return "Not found"

    post.pop("_id")

    return post


def get_many_posts():
    all_posts = list_posts()
    return all_posts


def add_post(*args):
    next_id = id_generator()
    new_entry = Post(next_id,*args).__dict__
    db.posts.insert_one(new_entry)

    return new_entry


def del_post(id: int):
    post_list = list_posts()
    id_list = [item["id"] for item in post_list]

    if not id in id_list:
        return False
    
    post_to_delete = get_one_post(id)

    db.posts.delete_one({"id":id})

    return post_to_delete


def upd_post(id : int, update_package : dict):
    post_list = list_posts()
    id_list = [item["id"] for item in post_list]

    if not id in id_list:
        return False

    data = db.posts.find_one({"id": id})
    update_items = {"$set" : update_package}
    db.posts.update_one(data, update_items)
    updated_post = get_one_post(id)

    return updated_post
