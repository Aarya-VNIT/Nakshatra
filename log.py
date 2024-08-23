import logging
import datetime
import os

from uploader import FileUploader

logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

DataLog: logging.Logger = logging.getLogger('data_log')
DataFileHandler = logging.FileHandler('data.csv')
DataFormatter = logging.Formatter('"%(asctime)s",%(message)s')

DataFileHandler.setFormatter(DataFormatter)

DataLog.handlers.clear()
DataLog.addHandler(DataFileHandler)

class Logger:

    CYCLE_COUNT: int = 1

    log: logging.Logger = logging.getLogger()
    file_handler: logging.FileHandler = None
    
    uploader: FileUploader = FileUploader()

    FORMAT_STRING = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(FORMAT_STRING)
    
    # Static code
    log.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    log.addHandler(console_handler)

    def get_logger():

        if 'log' not in os.listdir():
            os.mkdir('./log')
        
        if Logger.file_handler == None:
            Logger.file_handler = Logger.__get_log_file_handler(str(datetime.date.today()))
            Logger.log.addHandler(Logger.file_handler)
            
        else:
            
            try:                
                if Logger.file_handler.baseFilename.index(str(datetime.date.today())):
                    return Logger.log
                
            except ValueError:
                # Remove existing
                Logger.log.removeHandler(Logger.file_handler)
                
                # Create new one with today's date
                Logger.file_handler = Logger.__get_log_file_handler(str(datetime.date.today()))

                Logger.CYCLE_COUNT = 1
                
                # Attach the file handler to the log
                Logger.log.addHandler(Logger.file_handler)
        
        return Logger.log

    def __get_log_file_handler(name: str):
        
        file_handler = logging.FileHandler(f'./log/{name}.log')
        file_handler.setLevel(logging.DEBUG) 
        file_handler.setFormatter(Logger.formatter)
        
        return file_handler    