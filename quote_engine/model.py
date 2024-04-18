"""Model of quote class."""


class QuoteModel:
    """Implement quote model class."""

    def __init__(self, body: str, author: str):
        """Initialize QuoteModel."""
        self.author = author
        self.body = body

    def __str__(self) -> str:
        """User string representation for QuoteModel."""
        return f"Quote(body: {self.body}, author: {self.author})"

    def __repr__(self) -> str:
        """User representation for QuoteModel."""
        return f"Quote(body: {self.body}, author: {self.author})"
