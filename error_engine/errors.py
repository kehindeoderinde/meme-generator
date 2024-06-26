"""ERRORS FOR QUOTE ENGINE."""


class InvalidFileError(BaseException):
    """Invalid File Error."""

    def __init__(self, path: str):
        """Initialize InvalidFileError."""
        super().__init__(path)
        self.path = path

    def __str__(self) -> str:
        """User string representation of InvalidFileError."""
        return f'InvalidFileError(cause: "You can only upload CSV, PDF, PDF \
            and TXT files with the quote engine", path: {self.path})'


class InvalidFilePathError(BaseException):
    """Invalid File Path Error."""

    def __init__(self, path: str):
        """Initialize InvalidFilePathError."""
        super().__init__(path)
        self.path = path

    def __str__(self) -> str:
        """User string representation of InvalidFilePathError."""
        return f'InvalidFilePathError(cause: "File path specified \
            does not exist", path: {self.path})'


class InvalidTextInput(BaseException):
    """Limit text for body of quote."""

    def __init__(self, text, limit):
        """Initialize InvalidFileTextInput."""
        super().__init__(text)
        self.text = text
        self.limit = limit

    def __str__(self):
        """User string representation of InvalidTextInput."""
        return f'InvalidTextInput(cause: "Text entered too long. Maximum of \
            {self.limit} characters allowed", text: {self.text})'
