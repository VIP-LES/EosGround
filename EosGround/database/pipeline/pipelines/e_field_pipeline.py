from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosLib.format.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets

from EosGround.database.models.eos.e_field import EField

from EosLib.format.formats.e_field import EField as EField_Format

from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline


class EFieldPipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return PacketPipeline.get_notify_channel()

    @staticmethod
    def get_notify_channel() -> str | None:
        return None

    def extract(self, session: Session) -> Query:
        # to do: figure out enum for telemetry
        return session.query(ReceivedPackets).filter_by(packet_type=Type.E_FIELD, processed=False)\
            .order_by(ReceivedPackets.id)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming e_field_pipeline row id={record.id}")

        packet_data = EField_Format.decode(record.packet_body)
        packet_id = record.id
        a_voltage = packet_data.voltage_a
        b_voltage = packet_data.voltage_b
        c_voltage = packet_data.voltage_c
        insert_row = EField(
                              packet_id=packet_id,
                              a_voltage=a_voltage,
                              b_voltage=b_voltage,
                              c_voltage=c_voltage,
                                )
        record.processed = True
        session.add(insert_row)
