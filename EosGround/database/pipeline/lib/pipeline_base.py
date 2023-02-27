from abc import ABC, abstractmethod
from collections import namedtuple
from sqlalchemy import text
from sqlalchemy.orm import Query, Session, sessionmaker
import traceback

from EosGround.database.connect import connect


class PipelineBase(ABC):

    @staticmethod
    def enabled() -> bool:
        return True

    @staticmethod
    @abstractmethod
    def get_listen_channel() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_notify_channel() -> str | None:
        pass

    def __init__(self, config_filepath: str, debug_mode: bool):
        self.db_engine = connect(config_filepath, autoconnect=False, verbose=debug_mode)
        self.db = self.db_engine.connect()
        self.record_count = 0

    @abstractmethod
    def extract(self, session: Session) -> Query:
        pass

    @abstractmethod
    def transform(self, session: Session, record: namedtuple):
        pass

    def load(self, session: Session):
        session.commit()

        notify_channel = self.get_notify_channel()
        if notify_channel is not None:
            self.db.execute(text(f"NOTIFY f{notify_channel};"))
            self.db.commit()

    def run(self):

        self.db.execute(text(f"LISTEN {self.get_listen_channel()};"))
        print(f"listening for `NOTIFY {self.get_listen_channel()}`")
        while True:
            self.db.commit()
            self.db.connection.poll()
            while self.db.connection.notifies:
                self.db.connection.notifies.pop()
                session = sessionmaker(bind=self.db_engine)()
                try:
                    for record in self.extract(session):
                        self.transform(session, record)
                        self.record_count += 1
                    self.load(session)
                except Exception as e:
                    print(f"error occurred while processing record #{self.record_count}, rolling back:"
                          f" {e}\n{traceback.format_exc()}")
                    self.db.rollback()
