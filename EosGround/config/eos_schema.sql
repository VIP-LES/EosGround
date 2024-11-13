-- SCHEMA: eos_schema

-- DROP SCHEMA IF EXISTS eos_schema ;

CREATE SCHEMA IF NOT EXISTS eos_schema
    AUTHORIZATION pg_database_owner;

GRANT USAGE ON SCHEMA eos_schema TO PUBLIC;

GRANT ALL ON SCHEMA eos_schema TO pg_database_owner;

-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


--CREATE TABLE IF NOT EXISTS eos_schema.received_data
--(
--    id int NOT NULL GENERATED ALWAYS AS IDENTITY,
--    raw_bytes bytea NOT NULL,
--    rssi int NOT NULL,
--    processed boolean NOT NULL DEFAULT FALSE,
--    CONSTRAINT received_data_pkey PRIMARY KEY (id)
--);

CREATE TABLE IF NOT EXISTS eos_schema.received_data
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    raw_bytes bytea NOT NULL,
    rssi integer NOT NULL,
    processed boolean NOT NULL DEFAULT false,
    dropped boolean NOT NULL DEFAULT false,
    received_time timestamp without time zone,
    CONSTRAINT received_data_pkey PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS eos_schema.received_packets
(
    id int NOT NULL GENERATED ALWAYS AS IDENTITY,
    data_id int NOT NULL,
    packet_type int NOT NULL,
    sender int NOT NULL,
    priority int NOT NULL,
    destination int NOT NULL,
    generate_time timestamp without time zone NOT NULL,
    sequence_number int NOT NULL,
    send_time timestamp without time zone NOT NULL,
    received_time timestamp without time zone NOT NULL,
    packet_body bytea NOT NULL,
    processed boolean NOT NULL DEFAULT FALSE,
    CONSTRAINT received_packets_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS eos_schema.temperature
(
    id int NOT NULL GENERATED ALWAYS AS IDENTITY,
    packet_id int NOT NULL,
    temperature real NOT NULL,
    CONSTRAINT temperature_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS eos_schema.transmit_table
(
    id int NOT NULL GENERATED ALWAYS AS IDENTITY,
    time_sent timestamp without time zone,
    packet_type int NOT NULL,
    sender int NOT NULL,
    priority int NOT NULL,
    destination int NOT NULL,
    generate_time timestamp without time zone NOT NULL,
    body bytea NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS eos_schema.test_data
(
    id int NOT NULL GENERATED ALWAYS AS IDENTITY,
    packet_id int NOT NULL,
    random_int int,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS eos_schema.received_packets
    ADD CONSTRAINT received_packets_to_received_data FOREIGN KEY (data_id)
    REFERENCES eos_schema.received_data (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS eos_schema.temperature
    ADD CONSTRAINT temperature_to_received_packet FOREIGN KEY (packet_id)
    REFERENCES eos_schema.received_packets (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS eos_schema.test_data
    ADD CONSTRAINT test_data_to_received_packet FOREIGN KEY (packet_id)
    REFERENCES eos_schema.received_packets (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

-- Table: eos_schema.telemetry

-- DROP TABLE IF EXISTS eos_schema.telemetry;

CREATE TABLE IF NOT EXISTS eos_schema.telemetry
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    packet_id int NOT NULL,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- just added
    temperature double precision,
    pressure double precision,
    humidity double precision,
    x_rotation double precision,
    y_rotation double precision,
    z_rotation double precision,
    CONSTRAINT received_telemetry_data_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS eos_schema.telemetry
    ADD CONSTRAINT telemetry_to_received_packet FOREIGN KEY (packet_id)
    REFERENCES eos_schema.received_packets (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


-- Table: eos_schema.position

-- DROP TABLE IF EXISTS eos_schema."position";

CREATE TABLE IF NOT EXISTS eos_schema."position"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    packet_id integer NOT NULL,
    "timestamp" timestamp without time zone,
    latitude double precision,
    longitude double precision,
    altitude double precision,
    speed double precision,
    num_satellites integer,
    flight_state integer,
    CONSTRAINT position_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS eos_schema."position"
    ADD CONSTRAINT position_to_received_packet FOREIGN KEY (packet_id)
    REFERENCES eos_schema.received_packets (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


CREATE TABLE IF NOT EXISTS eos_schema.terminal_output
(
    id integer GENERATED ALWAYS AS IDENTITY,
    received_packet_id integer,
    transmit_table_id integer,
    terminal_output text COLLATE pg_catalog."default",
    CONSTRAINT terminal_output_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS eos_schema.terminal_output
    ADD CONSTRAINT terminal_to_received_packet FOREIGN KEY (received_packet_id)
    REFERENCES eos_schema.received_packets (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID,
    ADD CONSTRAINT terminal_to_transmit_table FOREIGN KEY (transmit_table_id)
    REFERENCES eos_schema.transmit_table (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


CREATE TABLE IF NOT EXISTS eos_schema.e_field
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    packet_id integer NOT NULL,
    a_voltage double precision,
    b_voltage double precision,
    c_voltage double precision,
    CONSTRAINT e_field_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS eos_schema.e_field
    ADD CONSTRAINT e_field_to_received_packet FOREIGN KEY (packet_id)
    REFERENCES eos_schema.received_packets (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

CREATE TABLE IF NOT EXISTS eos_schema."sensor_data"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    packet_id integer NOT NULL,
    "timestamp" timestamp without time zone,
    temperature_celsius double precision,  -- from SHTC3 temperature-humidity sensor
    relative_humidity_percent double precision,  -- from SHTC3 temperature-humidity sensor
    temperature_celsius_2 double precision,  -- from BMP388 temperature-pressure sensor
    pressure_hpa double precision,  -- from BMP388 temperature-pressure sensor
    altitude_meters double precision,  -- from BMP388 temperature-pressure sensor
    ambient_light_count integer,  -- from LTR390 uv-light sensor
    ambient_light_lux double precision,  -- from LTR390 uv-light sensor
    uv_count integer,  -- from LTR390 uv-light sensor
    uv_index double precision,  -- from LTR390 uv-light sensor
    infrared_count integer,  -- from TSL2591 ir-light sensor
    visible_count integer,  -- from TSL2591 ir-light sensor
    full_spectrum_count integer,  -- from TSL2591 ir-light sensor
    ir_visible_lux double precision,  -- from TSL2591 ir-light sensor
    pm10_standard_ug_m3 integer,  -- from PMSA003I particulate sensor
    pm25_standard_ug_m3 integer,  -- from PMSA003I particulate sensor
    pm100_standard_ug_m3 integer,  -- from PMSA003I particulate sensor
    pm10_environmental_ug_m3 integer,  -- from PMSA003I particulate sensor
    pm25_environmental_ug_m3 integer,  -- from PMSA003I particulate sensor
    pm100_environmental_ug_m3 integer,  -- from PMSA003I particulate sensor
    particulate_03um_per_01L integer,  -- from PMSA003I particulate sensor
    particulate_05um_per_01L integer,  -- from PMSA003I particulate sensor
    particulate_10um_per_01L integer,  -- from PMSA003I particulate sensor
    particulate_25um_per_01L integer,  -- from PMSA003I particulate sensor
    particulate_50um_per_01L integer,  -- from PMSA003I particulate sensor
    particulate_100um_per_01L integer,  -- from PMSA003I particulate sensor
    CONSTRAINT sensor_data_pkey PRIMARY KEY (id),
    CONSTRAINT fk_packet_id FOREIGN KEY (packet_id) REFERENCES eos_schema.received_packets(id)
);

END;

