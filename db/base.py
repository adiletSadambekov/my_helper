from dataclasses import dataclass

from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine


class CreateAndCloseSession:

    def __init__(self, engine: engine):
        Session = sessionmaker(engine)
        self.s = Session()

    def __del__(self):
        self.s.close_all()
