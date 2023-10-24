from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosLib.format.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets

from EosGround.database.models.eos.position import Position as Position_Model

from EosLib.format.formats.position import Position as Position_Format

from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline


class PositionPipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return PacketPipeline.get_notify_channel()

    @staticmethod
    def get_notify_channel() -> str | None:
        return None

    def extract(self, session: Session) -> Query:
        # to do: figure out enum for telemetry
        return session.query(ReceivedPackets).filter_by(packet_type=Type.POSITION, processed=False)\
            .order_by(ReceivedPackets.id)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming position_pipeline row id={record.id}")

        packet_data = Position_Format.decode(record.packet_body)
        packet_id = record.id
        time_stamp = packet_data.timestamp
        latitude = packet_data.latitude
        longitude = packet_data.longitude
        altitude = packet_data.altitude
        speed = packet_data.speed
        num_satellites = packet_data.number_of_satellites
        flight_state = packet_data.flight_state
        insert_row = Position_Model(
                              packet_id=packet_id,
                              latitude=latitude,
                              longitude=longitude,
                              altitude=altitude,
                              speed=speed,
                              num_satellites=num_satellites,
                              timestamp=time_stamp,
                              flight_state=flight_state)
        record.processed = True
        session.add(insert_row)
