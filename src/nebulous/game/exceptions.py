class NotSignedInError(Exception):
    """
    Raised when a user tries to perform an action that requires them to be signed in, but they are not signed in.
    """
    pass


class InvalidUserIDError(Exception):
    """
    Raised when a user ID is invalid.
    """
    pass
