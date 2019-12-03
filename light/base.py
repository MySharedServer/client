# -*- coding: utf-8 -*-
from rest_framework.generics import GenericAPIView
from django.http import QueryDict
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .utils import *
from logging import getLogger

logger = getLogger('django')


class Constants:
    DOWNLOAD = 'download'

    """API Kind Code"""
    API_KIND_DETAIL = 1

    """API Result Code"""
    SUCCESS = 0
    PARAMETER_ERROR = 101
    READ_ERROR = 201
    CONNECTION_ERROR = 202
    SEND_DATA_ERROR = 203
    PERMISSION_ERROR = 301
    EXCEPTION_EXIT = -1

    """ Dict key words"""
    KEY_RESULT = "result"
    KEY_DATA = "data"
    KEY_CURRENT_USER = "username"


class BaseAPIView(GenericAPIView):
    """
    Basic class for server API
    """

    def __init__(self):
        super(BaseAPIView, self).__init__()
        self.api_kind = None
        self.data_dict = {}
        self.user_name = ''
        self.result_dict = {Constants.KEY_RESULT: Constants.SUCCESS}

    def api_response(self, data=None, status_code=status.HTTP_200_OK):
        """
        This function is used to generate response for API.
        :param data:
        :param status_code:
        :return: Response
        """
        if data is not None:
            self.result_dict[Constants.KEY_DATA] = data
        return Response(data=self.result_dict, status=status_code)

    def set_api_result(self):
        """
        This function is used to set result code
        :return:
        """
        if self.api_kind == Constants.API_KIND_DETAIL:
            self.result_dict[Constants.KEY_RESULT] = Constants.READ_ERROR

    def get_parameter_dic(self, request):
        """
        This function is used to get request data to dict
        :param request: Django REST framework raw request
        :return: True or False
        """

        result = False

        try:
            if not isinstance(request, Request):
                return result

            query_params = request.query_params
            if isinstance(query_params, QueryDict):
                query_params = query_params.dict()
            result_data = request.data
            if isinstance(result_data, dict):
                result_data = result_data.get('data')
                if isinstance(result_data, str):
                    result_data = eval(result_data)

            if result_data is not None:
                self.data_dict = result_data
            else:
                self.data_dict = query_params.get('params', query_params)

            # convert string value
            if isinstance(self.data_dict, str):
                self.data_dict = eval(self.data_dict)
            elif isinstance(self.data_dict, dict):
                for key in self.data_dict:
                    if isinstance(self.data_dict[key], str) and self.data_dict[key].startswith(('[', '{')):
                        self.data_dict[key] = eval(self.data_dict[key])

            logger.info("{0}: params data:{1}".format(self.__class__.__name__, self.data_dict))
        except Exception as e:
            logger.info("{0}: parameter error:{1}".format(self.__class__.__name__, repr(e)))
        else:
            result = True
        return result

    def execute_custom_sql(self, sql=None):
        """
        This function is used to operate the database by sql
        :param sql:
        :return:
        """
        from django.db import connections
        from django.db.utils import DatabaseError, Error
        if sql is None:
            logger.info("{0}: sql is empty".format(self.__class__.__name__))
            return None

        logger.info("{0}: sql:{1}".format(self.__class__.__name__, sql))

        try:
            cursor = connections[settings.DATABASE].cursor()
            # query data
            cursor.execute(sql)
            # a = cursor.fetchall()
            rows = dict_fetch_all(cursor)
        except DatabaseError:
            logger.info("{0}: Database connect timeout occurred".format(self.__class__.__name__))
            rows = None
        except Error:
            logger.info("{0}: Operate database error occurred".format(self.__class__.__name__))
            rows = None

        return rows


class ClientAPIView(BaseAPIView):
    """
    Basic Recovery API, support 'GET' method
    """

    def get(self, request):
        """
        API 'GET' method for database 'read' operation
        Need to override get_queryset() function when extends
        :param request:
        :return:
        """

        self.api_kind = Constants.API_KIND_DETAIL
        self.user_name = request.META.get('REMOTE_USER', '')
        self.result_dict[Constants.KEY_CURRENT_USER] = self.user_name.split('\\')[-1]

        if self.get_parameter_dic(request):
            queryset = self.get_queryset()
            if queryset is None:
                self.set_api_result()
                response = self.api_response(status_code=status.HTTP_400_BAD_REQUEST)
            else:
                logger.info('{0}: query result count:{1}'.format(self.__class__.__name__, len(queryset)))
                response = self.api_response(queryset, status.HTTP_200_OK)
                if self.data_dict is not None and self.data_dict.get(Constants.DOWNLOAD, None):
                    response = data_to_csv(queryset)

        else:
            self.result_dict[Constants.KEY_RESULT] = Constants.PARAMETER_ERROR
            response = self.api_response(status_code=status.HTTP_400_BAD_REQUEST)
        logger.info("{0}: response:{1}".format(self.__class__.__name__, response))

        return response

    def post(self, request):
        """
        API 'POST' method for send command operation
        :param request:
        :return response:
        """

        self.api_kind = Constants.API_KIND_DETAIL

        if self.get_parameter_dic(request):
            if self.send_data():
                response = self.api_response({}, status_code=status.HTTP_200_OK)
            else:
                self.result_dict[Constants.KEY_RESULT] = Constants.SEND_DATA_ERROR
                response = self.api_response({}, status_code=status.HTTP_200_OK)
        else:
            self.result_dict[Constants.KEY_RESULT] = Constants.PARAMETER_ERROR
            response = self.api_response(status_code=status.HTTP_400_BAD_REQUEST)
        logger.info("{0}: response:{1}".format(self.__class__.__name__, response))

        return response

    def send_data(self):
        result = True
        logger.info('{0} send the command: {1}'.
                    format(self.__class__.__name__, result))
        return result
