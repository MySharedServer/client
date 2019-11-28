# -*- coding: utf-8 -*-
import csv
from django.http import HttpResponse
from logging import getLogger

logger = getLogger('django')


def dict_fetch_all(cursor):
    """
    Return all rows from a cursor as a dict
    :param cursor: database cursor
    :return: array dict
    """

    desc = cursor.description
    return [
        dict(zip([col[0].lower() for col in desc], row))
        for row in cursor.fetchall()
    ]


def data_to_csv(data_list=None):
    """
    convert query set to csv type data
    :param data_list: data set
    :return: response
    """
    if data_list is not None:
        try:
            response = HttpResponse(content_type=r'text\csv')
            response['Content-Disposition'] = 'attachment; filename="QueryData.csv"'
            writer = csv.writer(response)
            for index, data in enumerate(data_list):
                if index == 0:
                    writer.writerow(data.keys())
                    writer.writerow(data.values())
                else:
                    writer.writerow(data.values())
        except Exception as e:
            print("Write an CSV file, Case: %s" % e)

    return response
