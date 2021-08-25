
class Post:

    def __init__(self, id:int, created_at:str, updated_at:str, title: str, author:str, tags:list, content: str):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
