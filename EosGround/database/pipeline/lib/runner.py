from threading import Thread
import inspect
import time
import traceback

from EosGround.database.pipeline.lib.pipeline_base import PipelineBase
import EosGround.database.pipeline.pipelines as pipelines


class Runner:

    def __init__(self, config_filepath: str, debug_mode: bool):
        self.threads = {}
        self.config_filepath = config_filepath
        self.debug_mode = debug_mode

    def run(self) -> None:
        """ Enumerates over all the classes in the pipelines dir and spins them up """
        for attribute_name in dir(pipelines):
            pipeline = getattr(pipelines, attribute_name)
            try:
                if self.valid_pipeline(pipeline):
                    if pipeline.enabled():
                        print(f"spawning pipeline {pipeline.__name__}")
                        thread = Thread(
                            target=self._pipeline_runner,
                            args=(pipeline, self.config_filepath, self.debug_mode),
                            daemon=True
                        )
                        thread.start()
                        self.threads[pipeline.__name__] = thread
                    else:
                        print(f"not spawning invalid pipeline {pipeline.__name__}")
            except Exception as e:
                print(f"an error occurred while attempting to spawn pipeline f{pipeline.__name__}:"
                      f" {e}\n{traceback.format_exc()}")
        self._spin()

    @staticmethod
    def valid_pipeline(pipeline) -> bool:
        """ Determines if given class is a valid pipeline.

        :param pipeline: the class in question
        :return: True if valid, otherwise False
        """
        return (
                (pipeline is not None)
                and inspect.isclass(pipeline)
                and issubclass(pipeline, PipelineBase)
                and pipeline.__name__ != "PipelineBase"
        )

    @staticmethod
    def _pipeline_runner(cls, config_filepath: str, debug_mode: bool) -> None:
        """ Wrapper to execute pipeline run() method.

        :param cls: the pipeline class.  Must have a run() method
        """
        cls(config_filepath, debug_mode).run()

    @staticmethod
    def _spin() -> None:
        """ Spins to keep the software alive.  Never returns. """
        while True:
            time.sleep(10)
