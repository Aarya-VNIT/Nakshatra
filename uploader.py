import requests

class FileUploader:
    
    __URL = "http://projectnakshatra.pythonanywhere.com"
    
    def upload_file(self, file_path: str, timeout_seconds: int = 30) -> bool:        
        file = open(file_path)
        response = requests.post(FileUploader.__URL + "/upload", files={'file':file}, timeout = timeout_seconds)
        file.close()
        return response.status_code == 200

