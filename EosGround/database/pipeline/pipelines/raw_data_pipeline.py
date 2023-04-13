from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_data import ReceivedData
from EosGround.database.models.eos.received_packets import ReceivedPackets
from EosLib.packet.packet import Packet
from datetime import datetime


class PacketPipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return "packet_pipeline"

    @staticmethod
    def get_notify_channel() -> str | None:
        return "position_telemetry_pipeline"

    def extract(self, session: Session) -> Query:
        return session.query(ReceivedData).filter_by(processed=False).order_by(ReceivedData.id)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming raw_data_pipeline row id={record.id}")

        packet = Packet.decode(record.raw_bytes)
        data_type = packet.data_header.data_type
        sender = packet.data_header.sender
        priority = packet.data_header.priority
        destination = packet.data_header.destination
        generate_time = packet.data_header.generate_time

        sequence_num = packet.transmit_header.send_seq_num
        send_time = packet.transmit_header.send_time

        packet_body = packet.body

        received_time = record.received_time

        # update the row from table test1 to set processed=True
        record.processed = True

        # insert a new row into table test2
        insert_row = ReceivedPackets(data_id=record.id,
                                     packet_type=data_type,
                                     sender=sender,
                                     priority=priority,
                                     destination=destination,
                                     generate_time=generate_time,
                                     sequence_number=sequence_num,
                                     send_time=send_time,
                                     received_time=received_time,
                                     packet_body=packet_body)

        session.add(insert_row)
