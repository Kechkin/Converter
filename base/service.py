from datetime import datetime

from django.db.models import Avg, Q

from base.models import ExchangeRate
from django.db import connection


def search(data):
    if not data['time']:
        data['time'] = datetime.today()
    result = ExchangeRate.objects.get_course_value(data['time'], data['currency'])
    for i in result:
        context = {
            "data": {
                "currency": data['currency'],
                "time": i.pub_time,
                "value": i.value
            }
        }
        return context


def convert(data):
    if not data['time']:
        data['time'] = datetime.today()
    value1, value2 = None, None

    result = ExchangeRate.objects.filter(pub_time__lte=data['time'], currency=data['currency'])[:1].values(
        'value')
    for item in result:
        value1 = item['value']

    result2 = ExchangeRate.objects.filter(pub_time__lte=data['time'], currency=data['currency2'])[:1].values(
        'value')

    for item in result2:
        value2 = item['value']
    res_data = (data['money'] * value1) / value2
    ctx = {
        "data": {
            "currency": data['currency'],
            'time': data['time'],
            'result': "%.2f" % res_data
        }
    }
    return ctx


def find_average_orm(data):
    data_list, sum_of_values, count = {}, 0, 0

    if data['time']:  # if one day only
        result = ExchangeRate.objects.filter(
            Q(currency=data['currency'], pub_time__contains=data['time']) | Q(currency=data['currency2'],
                                                                              pub_time__contains=data[
                                                                                  'time'])).aggregate(Avg('value'))
        data_list[data['time']] = "%.2f" % result['value__avg']
        return data_list

    else:  # between two days
        result = ExchangeRate.objects.filter(
            Q(currency=data['currency'], pub_time__range=[data['start'], data['end']]) |
            Q(currency=data['currency2'], pub_time__range=[data['start'], data['end']]))
        for i in result:
            date = str(i.pub_time)[0:10]
            if date not in data_list:
                sum_of_values, count = i.value, 1
            else:
                count += 1
                sum_of_values += i.value
            data_list[date] = "%.2f" % (sum_of_values / count)
        return data_list


def find_average_raw(data):
    data_list = {}
    if data['time']:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT AVG(value) FROM base_exchangerate WHERE pub_time between %s'00:00:00' and %s'23:59:59' and ("
                "currency LIKE %s OR currency LIKE %s)",
                [data['time'], data['time'], data['currency'], data['currency2']])
            data_list[data['time']] = "%.2f" % cursor.fetchone()
            return data_list
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pub_time, value FROM base_exchangerate WHERE pub_time between %s'00:00:00' "
                "and %s'23:59:59' and ( "
                "currency LIKE %s OR currency LIKE %s) ORDER BY pub_time DESC",
                [data['start'], data['end'], data['currency'], data['currency2']])
            for item in cursor.fetchall():
                date = str(item[0])[0:10]
                if date not in data_list:
                    sum_of_values, count = item[1], 1
                else:
                    count += 1
                    sum_of_values += item[1]
                data_list[date] = "%.2f" % (sum_of_values / count)
            return data_list

