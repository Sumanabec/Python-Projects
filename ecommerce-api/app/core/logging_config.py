import logging

def set_logger():
    logging.basicConfig(
        filename="logs/app.log",
        filemode='a',
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
