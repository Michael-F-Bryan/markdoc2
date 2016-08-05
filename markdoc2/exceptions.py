
class MarkdocError(Exception):
    pass

class InvalidFileName(MarkdocError):
    """
    Error raised when someone names a file "index.*"
    """
