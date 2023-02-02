class oAuthRespone():
    SUCCESS = 0
    ERROR = 1
    INVALID = 2
    JSON_ERROR = 3
    REQUEST_ERROR = 4

    def __str__(self):
        return f"oAuthRespone({str(self.value)})"


class oAuthTypes():
    GOOGLE = 0

    def __str__(self):
        return f"oAuthTypes({str(self.value)})"