
import os

class add_path():
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.old_path = os.environ['PATH']
        os.environ['PATH'] = self.path + os.pathsep + self.old_path

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ['PATH'] = self.old_path
        
