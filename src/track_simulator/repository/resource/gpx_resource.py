import abc


class GPXResource(abc.ABC):

    def read(self, file_path):
        pass

    def write(self, uid, data):
        pass