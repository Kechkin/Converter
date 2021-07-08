from datetime import datetime

from django.db.models import Avg

from base.models import ExchangeRate


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
    sum_of_values, count, data_list = 0, 0, {}
    if data['time']:  # if one day only
        result = ExchangeRate.objects.filter(pub_time__contains=data['time'],
                                             currency=data['currency']).aggregate(Avg('value'))
        data_list[data['time']] = "%.2f" % (result['value__avg'])
        return data_list
    else:  # between two days
        for item in ExchangeRate.objects.filter(pub_time__range=[data['start'], data['end']],
                                                currency=data['currency']):
            date = str(item.pub_time)[0:10]
            if date not in data_list:  # get an average value in every day
                sum_of_values, count = item.value, 1
            else:
                count += 1
                sum_of_values += item.value
            data_list[date] = "%.2f" % (sum_of_values / count)
        return data_list


def find_average_raw(data):
    sum_of_values, count, data_list = 0, 0, {}
    if data['time']:
        res_data = ExchangeRate.objects.raw("SELECT * FROM base_exchangerate WHERE currency = %s And pub_time BETWEEN "
                                            "%s'00:00:00' And %s'23:59:59'",
                                            [data['currency'], data['time'], data['time']])
        for item in res_data:
            count += 1
            sum_of_values += item.value
            data_list[data['time']] = "%.2f" % (sum_of_values / count)
        return data_list
    else:
        res_data = ExchangeRate.objects.raw("SELECT * FROM base_exchangerate WHERE currency = %s And pub_time "
                                            "BETWEEN "
                                            "%s And %s ORDER BY pub_time DESC",
                                            [data['currency'], data['start'], data['end']])
        for item in res_data:
            date = str(item.pub_time)[0:10]
            if date not in data_list:
                sum_of_values, count = item.value, 1
            else:
                count += 1
                sum_of_values += item.value
            data_list[date] = "%.2f" % (sum_of_values / count)
        return data_list
