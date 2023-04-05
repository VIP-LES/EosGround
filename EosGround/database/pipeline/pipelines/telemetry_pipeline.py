from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosLib.packet.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets
from EosGround.database.models.eos.telemetry import Telemetry
from EosLib.format.telemetry_data import TelemetryData

from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline


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


class TelemetryPipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return PacketPipeline.get_notify_channel()

    @staticmethod
    def get_notify_channel() -> str | None:
        return None

    def extract(self, session: Session) -> Query:
        # to do: figure out enum for telemetry
        return session.query(ReceivedPackets).filter_by(packet_type=Type.TELEMETRY_DATA, processed=False)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming telemetry_pipeline row id={record.id}")
        record.processed = True
        packet_data = TelemetryData.decode_data(record.packet_body)
        packet_id = record.id
        timestamp = packet_data.timestamp
        temperature = packet_data.temperature
        pressure = packet_data.pressure
        humidity = packet_data.humidity
        x_rotation = packet_data.x_rotation
        y_rotation = packet_data.y_rotation
        z_rotation = packet_data.z_rotation

        insert_row = Telemetry(timestamp=timestamp,
                               packet_id=packet_id,
                               temperature=temperature,
                               pressure=pressure,
                               humidity=humidity,
                               x_rotation=x_rotation,
                               y_rotation=y_rotation,
                               z_rotation=z_rotation)

        session.add(insert_row)
