"""IMAGE MODEL."""


class ImageModel:
    """Helper class to store Image path as class."""

    def __init__(self, name, parent_dir) -> None:
        """Initialize ImageModel."""
        self.name = name
        self.parent_dir = parent_dir

    def __repr__(self) -> str:
        """User representation of ImageModel."""
        return f"Image(parent_dir: {self.parent_dir}, name: {self.name})"
