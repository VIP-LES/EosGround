from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosLib.format.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets

from EosGround.database.models.eos.downlink_chunk import DownlinkChunk

from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat

from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline


class DownlinkChunkPipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return PacketPipeline.get_notify_channel()

    @staticmethod
    def get_notify_channel() -> str | None:
        return None

    def extract(self, session: Session) -> Query:
        # to do: figure out enum for telemetry
        return session.query(ReceivedPackets).filter_by(packet_type=Type.DOWNLINK_CHUNK, processed=False)\
            .order_by(ReceivedPackets.id)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming downlink_chunk_pipeline row id={record.id}")

        packet_data = DownlinkChunkFormat.decode(record.packet_body)
        packet_id = record.id
        chunk_num = packet_data.chunk_num
        chunk_body = packet_data.chunk_body

        insert_row = DownlinkChunk(
                              packet_id=packet_id,
                              chunk_num=chunk_num,
                              chunk_body=chunk_body)
        record.processed = True
        session.add(insert_row)
