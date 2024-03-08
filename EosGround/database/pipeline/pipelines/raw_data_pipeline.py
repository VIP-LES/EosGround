from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_data import ReceivedData
from EosGround.database.models.eos.received_packets import ReceivedPackets
from EosLib.packet.packet import Packet
from datetime import datetime


class PacketPipeline(PipelineBase):

    # defines which string to listen for to start the pipeline

    @staticmethod
    def get_listen_channel() -> str:
        return "packet_pipeline"

    # once the pipeline completes the tranformation it releases a
    #notify message to start the next pipeline
    @staticmethod
    def get_notify_channel() -> str | None:
        return "post_packet_pipeline"

    # takes the data from the source table and filters by records that
    # have not been processed
    def extract(self, session: Session) -> Query:
        return session.query(ReceivedData).filter_by(processed=False).order_by(ReceivedData.id)

    # unpacks the data from the raw bytes in the ReceivedData table
    # places the attributes of the packet into ReceivedPackets table
    def transform(self, session: Session, record: namedtuple):
        print(f"transforming raw_data_pipeline row id={record.id}")

        try:
            packet = Packet.decode(record.raw_bytes)

            data_type = packet.data_header.data_type
            sender = packet.data_header.sender
            priority = packet.data_header.priority
            destination = packet.data_header.destination
            generate_time = packet.data_header.generate_time

            sequence_num = packet.transmit_header.send_seq_num
            send_time = packet.transmit_header.send_time

            packet_body = packet.body.encode()

            received_time = record.received_time

            # update the row from table ReceivedData to set processed=True
            record.processed = True

            # insert a new row into table ReceivedPackets
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
        except:
            record.dropped = True

