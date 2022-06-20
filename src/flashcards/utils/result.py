class Result:
    """Represent the outcome of an operation"""

    def __init__(self, success, value, error):
        self.success = success
        self.value = value,
        self.error = error

    def __str__(self):
        if self.success:
            return "[Success]"
        else:
            return f"[Failure] {self.error}"

    def __repr__(self):
        if self.success:
            return f"<Result success={self.success}>"
        else:
            return f'<Result success={self.success}, message="{self.error}">'

    @property
    def failure(self):
        return not self.success

    @staticmethod
    def Fail(error_message):
        return Result(False, value=None, error=error_message)

    @staticmethod
    def Ok(value=None):
        return Result(True, value=value, error=None)
