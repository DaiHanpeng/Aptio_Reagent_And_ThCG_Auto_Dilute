import logging, logging.handlers


class ProjetLogger(object):
    def __init__(self):
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)
        logfile = logging.handlers.TimedRotatingFileHandler("logging" , 'midnight', 1, backupCount=30)
        logfile.suffix = "%Y%m%d.log"
        logfile.setLevel(logging.DEBUG)
        logfile.setFormatter(logging.Formatter('%(asctime) s %(module)s: %(message)s'))
        self.logger.addHandler(logfile)

    def write_log_message(self, message):
        self.logger.debug(message)


project_logger = ProjetLogger()


if __name__ == "__main__":
    project_logger.write_log_message("hello")
    project_logger.write_log_message("this is Dai!")
