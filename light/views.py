from .base import ClientAPIView
from logging import getLogger

logger = getLogger('django')


# Create your views here.
class Demo(ClientAPIView):
    """
    Demo
    """

    def __init__(self):
        super(ClientAPIView, self).__init__()

    def get_queryset(self):
        resp = {
            'param': 'Hello wold'
        }
        return resp

    def send_data(self):
        result = True
        logger.info('{0} send the command: {1}'.
                    format(self.__class__.__name__, result))
        return result
