import os

class add_path():
    """ Utility class for adding temporary system path variables """
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.old_path = os.environ['PATH']
        os.environ['PATH'] = self.path + os.pathsep + self.old_path

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ['PATH'] = self.old_path
        
def find_binary(dir, bin_name):
    """returns directory of binary"""
    if bin_name:
        for root, dirs, files in os.walk(dir):
            for file in files:
                file_name , file_extension = os.path.splitext(file)
                if bin_name == file_name and os.path.isfile(os.path.join(root, file)):
                    return os.path.join(root)
    return None