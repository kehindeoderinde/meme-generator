'''Model of quote class'''

class QuoteModel:
    '''Implement quote model class'''
    def __init__(self, body: str, author: str):
        self.author = author
        self.body = body
        
    def __str__(self) -> str:
        return f'Quote(body: {self.body}, author: {self.author})'
    
    def __repr__(self) -> str:
        return f'Quote(body: {self.body}, author: {self.author})'