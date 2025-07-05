# from src.logger import configure_logger
# from src.exception import MyException

# logger = configure_logger("custom")

# try:
#     x = 1 + "a"  # will raise TypeError
# except Exception as e:
#     logger.error("Exception occurred", exc_info=True)
#     raise MyException(e) from e


from src.pipeline.training_pipeline import TrainPipeline

p = TrainPipeline()
p.run_pipeline()


#dds