from collections import namedtuple

from EosLib.packet import Packet
from sqlalchemy.orm import Query, Session

from EosLib.format.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets

from EosGround.database.models.eos.terminal_output import TerminalOutput
from EosLib.format.formats.cutdown import CutDown
from EosLib.format.formats.ping_format import Ping
from EosLib.format.decode_factory import decode_factory


from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline


class TerminalPipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return PacketPipeline.get_notify_channel()

    @staticmethod
    def get_notify_channel() -> str | None:
        return None

    def extract(self, session: Session) -> Query:
        commands = [Type.CUTDOWN, Type.PING, Type.VALVE, Type.HEALTH_QUERY_COMMAND]
        return session.query(ReceivedPackets).filter(ReceivedPackets.packet_type.in_(commands), ReceivedPackets.processed == False)\
            .order_by(ReceivedPackets.id)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming terminal_output_pipeline row id={record.id}")
        received_packet_id = record.id

        packet_body = decode_factory.decode(record.packet_type, record.packet_body)

        terminal_output = packet_body.to_terminal_output_string()
        transmit_table_id = None
        insert_row = TerminalOutput(
                                received_packet_id=received_packet_id,
                                terminal_output=terminal_output,
                                transmit_table_id=transmit_table_id
                              )
        record.processed = True
        session.add(insert_row)
