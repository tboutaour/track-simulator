import abc

class GraphInformationRepository(abc.ABC):

    @abc.abstractmethod
    def read_graph_information_dataframe(self, id_track):
        """
        Method to get graph information in DataFrame format from conection to resource.

        :param id_track: id of the element to retrieve.
        """
        pass

    @abc.abstractmethod
    def write_graph_information_dataframe(self, data):
        """
        Method to store graph information in DataFrame format into a resource.


        :param data: DataFrame to store.
        """
        pass
