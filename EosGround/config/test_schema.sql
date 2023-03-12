-- test_schema is a place for fake tables for testing/demo purposes


-- create schema

CREATE SCHEMA IF NOT EXISTS test_schema
    AUTHORIZATION pg_database_owner;

GRANT USAGE ON SCHEMA test_schema TO PUBLIC;

GRANT ALL ON SCHEMA test_schema TO pg_database_owner;


-- create tables

BEGIN;

CREATE TABLE IF NOT EXISTS test_schema.test1
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    random_number integer,
    processed boolean NOT NULL DEFAULT false,
    CONSTRAINT test1_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS test_schema.test2
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    random_number integer,
    test1_id bigint,
    CONSTRAINT test2_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS test_schema.test2
    ADD CONSTRAINT test2_test1_fkey FOREIGN KEY (test1_id)
    REFERENCES test_schema.test1 (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;
