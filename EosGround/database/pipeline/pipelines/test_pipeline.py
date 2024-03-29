from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.test.test1 import Test1
from EosGround.database.models.test.test2 import Test2


# Test SQL (run from pgAdmin after starting pipeline):
#
# BEGIN;
#
# INSERT INTO test_schema.test1 (random_number)
# VALUES (1), (2), (3);
#
# NOTIFY test_start;
#
# COMMIT;


class TestPipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return "test_start"

    @staticmethod
    def get_notify_channel() -> str | None:
        return "test_done"

    def extract(self, session: Session) -> Query:
        return session.query(Test1).filter_by(processed=False)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming test1 row id={record.id}")
        # update the row from table test1 to set processed=True
        record.processed = True
        # insert a new row into table test2
        transformed_random_number = 42 + record.random_number
        insert_row = Test2(random_number=transformed_random_number, test1_id=record.id)
        session.add(insert_row)
