from sqlalchemy import Identity, Integer, ForeignKey, DOUBLE_PRECISION, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from EosGround.database.models import TableBase
from EosGround.database.models.eos import SCHEMA

# import datetime

class Science(TableBase):
    __tablename__ = 'telemetry'
    __table_args__ = {'schema': SCHEMA}

    temperature_celsius: Mapped[float] = mapped_column(DOUBLE_PRECISION)  # from SHTC3 temperature-humidity sensor
    relative_humidity_percent: Mapped[float] = mapped_column(DOUBLE_PRECISION)  # from SHTC3 temperature-humidity sensor
    temperature_celsius_2: Mapped[float] = mapped_column(DOUBLE_PRECISION)  # from BMP388 temperature-pressure sensor
    pressure_hpa: Mapped[float] = mapped_column(DOUBLE_PRECISION)  # from BMP388 temperature-pressure sensor
    altitude_meters: Mapped[float] = mapped_column(DOUBLE_PRECISION)  # from BMP388 temperature-pressure sensor
    ambient_light_count: Mapped[int] = mapped_column(Integer)  # from LTR390 uv-light sensor
    ambient_light_lux: Mapped[float] = mapped_column(DOUBLE_PRECISION)  # from LTR390 uv-light sensor
    uv_count: Mapped[int] = mapped_column(Integer)  # from LTR390 uv-light sensor
    uv_index: Mapped[float] = mapped_column(DOUBLE_PRECISION)  # from LTR390 uv-light sensor
    infrared_count: Mapped[int] = mapped_column(Integer)  # from TSL2591 ir-light sensor
    visible_count: Mapped[int] = mapped_column(Integer)  # from TSL2591 ir-light sensor
    full_spectrum_count: Mapped[int] = mapped_column(Integer)  # from TSL2591 ir-light sensor
    ir_visible_lux: Mapped[float] = mapped_column(DOUBLE_PRECISION)  # from TSL2591 ir-light sensor
    pm10_standard_ug_m3: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    pm25_standard_ug_m3: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    pm100_standard_ug_m3: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    pm10_environmental_ug_m3: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    pm25_environmental_ug_m3: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    pm100_environmental_ug_m3: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    particulate_03um_per_01L: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    particulate_05um_per_01L: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    particulate_10um_per_01L: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    particulate_25um_per_01L: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    particulate_50um_per_01L: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
    particulate_100um_per_01L: Mapped[int] = mapped_column(Integer)  # from PMSA003I particulate sensor
