import traceback

from collections import namedtuple
from sqlalchemy.orm import Query, Session

from EosLib.format.definitions import Type

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
from EosGround.database.models.eos.received_packets import ReceivedPackets


from EosLib.format.formats.science_data import ScienceData

from EosGround.database.pipeline.pipelines.raw_data_pipeline import PacketPipeline


class SciencePipeline(PipelineBase):

    @staticmethod
    def get_listen_channel() -> str:
        return PacketPipeline.get_notify_channel()

    @staticmethod
    def get_notify_channel() -> str | None:
        return None

    def extract(self, session: Session) -> Query:
        return session.query(ReceivedPackets).filter_by(packet_type=Type.SCIENCE_DATA, processed=False)

    def transform(self, session: Session, record: namedtuple):
        try:
            print(f"printing science_data row id={record.id}")
            packet_data = ScienceData.decode(record.packet_body)
            data = [
                packet_data.temperature_celsius,
                packet_data.relative_humidity_percent,
                packet_data.temperature_celsius_2,
                packet_data.pressure_hpa,
                packet_data.altitude_meters,
                packet_data.ambient_light_count,
                packet_data.ambient_light_lux,
                packet_data.uv_count,
                packet_data.uv_index,
                packet_data.infrared_count,
                packet_data.visible_count,
                packet_data.full_spectrum_count,
                packet_data.ir_visible_lux,
                packet_data.pm10_standard_ug_m3,
                packet_data.pm25_standard_ug_m3,
                packet_data.pm100_standard_ug_m3,
                packet_data.pm10_environmental_ug_m3,
                packet_data.pm25_environmental_ug_m3,
                packet_data.pm100_environmental_ug_m3,
                packet_data.particulate_03um_per_01L,
                packet_data.particulate_05um_per_01L,
                packet_data.particulate_10um_per_01L,
                packet_data.particulate_25um_per_01L,
                packet_data.particulate_50um_per_01L,
                packet_data.particulate_100um_per_01L]

            out = ""
            for d in data:
                out += str(d) + ', '
            out = out[:-2]

            record.processed = True

            print(out)
        except Exception as e:
            print(f"An unhandled exception occurred while printing science data: {e}\n{traceback.format_exc()}")
