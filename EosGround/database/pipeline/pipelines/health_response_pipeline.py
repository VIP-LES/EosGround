from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosLib.format.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets

# from EosGround.database.models.eos.health_query import HealthQuery

from EosLib.format.formats.health.driver_health_report import DriverHealthReport

from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline

from EosGround.database.models.eos.health_report import HealthReport


class HealthResponsePipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return PacketPipeline.get_notify_channel()

    @staticmethod
    def get_notify_channel() -> str | None:
        return None

    def extract(self, session: Session) -> Query:
        # Should packet_type be Driver_health_report or health_query?
        return session.query(ReceivedPackets).filter_by(packet_type=Type.DRIVER_HEALTH_REPORT, processed=False)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming health_response_pipeline row id={record.id}")
        packet_data = DriverHealthReport.decode(record.packet_body)
        packet_id = record.id
        device_id = record.device_id
        health_report = record.health_report

        insert_row = HealthReport(
                                    packet_id=packet_id,
                                    device_id=device_id,
                                    health_report=health_report,

                                )
        record.processed = True
        session.add(insert_row)



