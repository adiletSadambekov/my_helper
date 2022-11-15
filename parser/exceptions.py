


class ReceivedIncorrectResponse(Exception):
    def __init__(self, status_code: int):
        self.message = f'Getting response with code \
            {str(status_code)}. required response with code 200'
    
    def __str__(self) -> str:
        return self.message