

class ErrorAddUser(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ErrorParametrs(Exception):
    def __init__(self, *args) -> None:
        if args[0]:
            self.message = str(args[0])
        else:
            self.message = 'Function required minimun one argument'
        super().__init__(self.message)