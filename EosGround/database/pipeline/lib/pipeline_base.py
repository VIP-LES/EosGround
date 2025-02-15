from abc import ABC, abstractmethod
from collections import namedtuple
from sqlalchemy import text
from sqlalchemy.orm import Query, Session, sessionmaker
import traceback

from EosGround.database.connect import connect
from EosGround.database.connect import connect_docker


class PipelineBase(ABC):

    @staticmethod
    def enabled() -> bool:
        """ [OPTIONAL] Defaults to True.

        :return: True if driver is enabled, False otherwise
        """
        return True

    @staticmethod
    @abstractmethod
    def get_listen_channel() -> str:
        """ [REQUIRED] Returns the postgres channel that will trigger the pipeline.
        ie if the trigger process issues "NOTIFY david", then this function should return "david"

        :return: the name of the postgres channel that will trigger the pipeline
        """
        pass

    @staticmethod
    @abstractmethod
    def get_notify_channel() -> str | None:
        """ [REQUIRED] Returns a channel to notify at the end of the load().  If you don't want to, return None

        :return: the name of the postgres channel to trigger at the end of the pipeline
        """
        pass

    def __init__(self, config_filepath: str, debug_mode: bool):
        """ sets up the database connection
        If you choose to override this method, calling `super().__init__(output_directory)`
        at the beginning is required.
        """
        self.db_engine = connect_docker(config_filepath, autoconnect=False, verbose=debug_mode)
        self.db = self.db_engine.connect()
        self.record_count = 0

    @abstractmethod
    def extract(self, session: Session) -> Query:
        """ [REQUIRED] Extracts the relevant data out of the database

        :param session: the query session
        :return: the sqlalchemy SELECT query to execute.
        """
        pass

    @abstractmethod
    def transform(self, session: Session, record: namedtuple) -> None:
        """ [REQUIRED] Performs the transformations to the data.  Modifying record will automatically generate an
        UPDATE.  Using session.add or session.add_all automatically generates INSERTs.

        :param session: the query session
        :param record: an individual record of whatever you extracted in extract()
        """
        pass

    def load(self, session: Session) -> None:
        """ Commits the changes back to the database and issues a NOTIFY if get_notify_channel() returns non-None.
        This method exists so that in the event we want to do other things with the output than save back to DB,
        we can just override this.

        :param session: the query session
        """
        session.commit()

        notify_channel = self.get_notify_channel()
        if notify_channel is not None:
            self.db.execute(text(f"NOTIFY {notify_channel};"))
            self.db.commit()

    def run(self) -> None:
        """ Main method for the data pipeline.  Do not override this method. """
        self.db.execute(text(f"LISTEN {self.get_listen_channel()};"))
        print(f"listening for `NOTIFY {self.get_listen_channel()}`")
        while True:
            self.db.commit()
            self.db.connection.poll()
            while self.db.connection.notifies:
                self.db.connection.notifies.pop()
                session = sessionmaker(bind=self.db_engine)()
                try:
                    start_count = self.record_count
                    for record in self.extract(session):
                        self.transform(session, record)
                        self.record_count += 1
                    self.load(session)
                    print(f"successfully processed {self.record_count - start_count} records")
                except Exception as e:
                    print(f"error occurred while processing record #{self.record_count}, rolling back:"
                          f" {e}\n{traceback.format_exc()}")
                    self.db.rollback()
