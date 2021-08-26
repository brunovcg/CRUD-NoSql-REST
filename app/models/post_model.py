from datetime import datetime
class Post:

        
    def __init__(self, id:int, title: str, author:str, tags:list, content: str):
        self.id = id
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
        self.created_at = datetime.utcnow()
        self.updated_at = "only created, not update yet"
