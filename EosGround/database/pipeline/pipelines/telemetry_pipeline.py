from collections import namedtuple
from sqlalchemy.orm import Query, Session

import datetime

from EosLib.format.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets
from EosGround.database.models.eos.telemetry import Telemetry


from EosLib.format.formats.telemetry_data import TelemetryData

from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline


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
        packet_data = TelemetryData.decode(record.packet_body)
        packet_id = record.id
        timestamp = datetime.datetime.now()
        temperature = packet_data.temperature
        pressure = packet_data.pressure
        humidity = packet_data.humidity
        x_rotation = packet_data.x_rotation
        y_rotation = packet_data.y_rotation
        z_rotation = packet_data.z_rotation

        insert_row = Telemetry(
                               packet_id=packet_id,
                               timestamp=timestamp,
                               temperature=temperature,
                               pressure=pressure,
                               humidity=humidity,
                               x_rotation=x_rotation,
                               y_rotation=y_rotation,
                               z_rotation=z_rotation)

        record.processed = True

        session.add(insert_row)
