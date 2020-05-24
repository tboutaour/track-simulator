import abc


class TrackInformationRepository(abc.ABC):

    @abc.abstractmethod
    def get_trackinformation_dataframe(self, id_track):
        """
        Method to get track information from a resource.
        :param id_track: id of track to obtain.
        """
        pass

    @abc.abstractmethod
    def write_trackinformation_dataframe(self, id_track, data):
        """
        Method to store track information in DataFrame format into a resource.
        :param id_track: id to identify the information in the resource.
        :param data:
        """
        pass

    @abc.abstractmethod
    def write_trackinformation_dataframes(self, data):
        """
        Method to store more than one dataframe into the resource.
        :param data: data to store in DataFrame format.
        """
        pass

