from collections import namedtuple
from sqlalchemy.orm import Query, Session
import psycopg2
import os
from threading import Lock

from EosLib.format.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets

from EosGround.database.models.eos.downlink_command import DownlinkCommand as DownlinkCommandModel

from EosLib.format.formats.downlink_header_format import DownlinkCommandFormat

from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline

from EosGround.config.config import get_config


class DownlinkCommandPipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return PacketPipeline.get_notify_channel()

    @staticmethod
    def get_notify_channel() -> str | None:
        return None

    def extract(self, session: Session) -> Query:
        # to do: figure out enum for telemetry
        return session.query(ReceivedPackets).filter_by(packet_type=Type.DOWNLINK_COMMAND, processed=False)\
            .order_by(ReceivedPackets.id)

    def transform(self, session: Session, record: namedtuple):
        print(f"transforming downlink_command_pipeline row id={record.id}")

        packet_data = DownlinkCommandFormat.decode(record.packet_body)
        packet_id = record.id
        file_id = packet_data.file_id
        num_chunks = packet_data.num_chunks
        command_type = packet_data.command_type
        missing_chunks = packet_data.missing_chunks
        insert_row = DownlinkCommandModel(
            packet_id=packet_id,
            file_id=file_id,
            num_chunks=num_chunks,
            command_type=command_type,
            missing_chunks=missing_chunks)
        record.processed = True
        session.add(insert_row)
