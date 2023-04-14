# Data Pipelines

## About
EosGround receives thousands of radio packets from the payload in the course of flight.  These are received as raw binary data, which is incredibly not useful for the ground station application.  There are many data types and formats, which are best represented by individual database tables.  The process of extracting and transforming the raw binary into tidy tables is performed by a set of data pipeline scripts, which live in the `EosGround.database.pipeline` python module.

### How do pipelines work?
Each pipeline does three things:
1. extracts data from one place (extract!)
2. makes some transformations to it (transform!)
3. puts in a new place (load!)

Pipelines are triggered using the postgres NOTIFY / LISTEN feature.  Any process that issues a `NOTIFY <channel>;` message will trigger any process that is running `LISTEN <channel>;`.  Each pipeline defines a channel that triggers it and optionally a channel to notify upon the pipeline finishing.

Most of the actual motion is done by the PipelineBase class, which all pipelines extend, in the run method.

The Runner is the entry point and is responsible for spawning all pipelines.  It loads each pipleine in the `EosGround.database.pipeline.pipelines` module, and runs them as a thread.

Most SQL things are done using the Sqlalchemy ORM.

## Running the Pipelines
From the repository root, run `python -m EosGround.database.pipeline`.  You can optionally pass the `-d` flag to run with verbose output, which is useful to print all the actual SQL being run  
NOTE: if you only want to run specific pipelines, you can override the `enabled()` method to return false on the pipelines you don't want to run

## Development
### Making A New Pipeline
1. Have the relevant tables been defined in `EosGround.database.models`?  If not go do that
2. Make a new class in `EosGround.database.pipeline.pipelines` that extends `EosGround.database.pipeline.lib.pipeline_base`
3. Define the `get_listen_channel()` and `get_notify_channel()` methods.  You can return None for the notify channel if you don't wish to notify after the pipeline finishes
4. Define the `extract()` method.  This is the method that pulls the relevant data out of the database.  You basically just build and return a SQL SELECT query
5. Define the `transform()` method.  This method gives you a single results row from `extract()`, which you can then modify or use to build a new insert.  Any changes you make to the input record will be processed as a SQL update, and any objects you create using `session.add()` / `session.add_all()` will be processed as SQL inserts.
6. Done!  Just gotta test

### Working Example
See `EosGround.database.pipeline.pipelines.test_pipeline`
