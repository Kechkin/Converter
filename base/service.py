from datetime import datetime
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
