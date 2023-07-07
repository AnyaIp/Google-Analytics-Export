class envfilePthException(Exception):
    "Raised when environment file does not exist"
    pass

class authException(Exception):
    "Raised when variable required for auth does not exist"
    pass

class resultException(Exception):
    "Raised when it is failed to return results"
    pass