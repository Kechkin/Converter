import base64
import json
from datetime import datetime
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from base.forms import *


def check_user(func):
    def wrapped(request, *args):
        if request.user.is_authenticated:
            return func(request, *args)
        else:
            if 'HTTP_AUTHORIZATION' in request.META:
                user_data = request.META['HTTP_AUTHORIZATION'].split()
                username, password = (base64.b64decode(user_data[1])).decode().split(":")
                user = User.objects.get(username=username)
                if user.is_active:
                    return func(request)
        return HttpResponse('Unauthorized', status=401)

    return wrapped


def check_http(request_list):
    def wrapped(func):
        def inner(request, *args):
            if request.method in request_list:
                return func(request, *args)
            return HttpResponse(f"{request.method} method not allowed")

        return inner

    return wrapped


@check_http(["POST", "GET"])
def register_page(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, "base/register.html", {"form": form})


@check_http(["POST", "GET"])
def user_login(request):
    form = UserLoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, "base/login.html", {"form": form})


@check_http(["POST", "GET"])
@check_user
def index(request):
    context = {
        "add": Add_data(),
        "search": Search_data(),
        "convert": Convert_data()
    }
    return render(request, "base/index.html", context)


@check_http(["POST"])
@check_user
def add(request):
    form = Add_data(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')
    return HttpResponse("Error")


@check_http(['POST'])
@check_user
def api_add(request):
    data = json.loads(request.body)
    form = Add_data(data)
    if form.is_valid():
        form.save()
        return JsonResponse({"Status": HttpResponse.status_code})
    return JsonResponse({"Response": "400"})


@check_http(['POST'])
@check_user
def api_search(request):
    data_json = json.loads(request.body)
    form = Search_data(data_json)
    if form.is_valid():
        data = form.cleaned_data
        return search(request, data)
    return JsonResponse({"Response": "400"})


@check_user
@check_http(['POST'])
def api_convert(request):
    data_json = json.loads(request.body)
    form = Convert_data(data_json)
    if form.is_valid():
        data = form.cleaned_data
        return convert(request, data)
    return JsonResponse({"Response": "400"})


@check_http(["POST"])
@check_user
def search(request, data=None):
    form = Search_data(request.POST)
    if data is None and form.is_valid():
        data = form.cleaned_data
    if not data['time']:
        data['time'] = datetime.today()
    result = ExchangeRate.objects.get_course_value(data['time'], data['currency'])
    for i in result:
        context = {
            "Status": HttpResponse.status_code,
            "data": {
                "currency": data['currency'],
                "time": i.pub_time,
                "value": i.value
            }
        }
        return JsonResponse(context)
    return HttpResponse("There's no value or currency")


@check_http(["POST"])
@check_user
def convert(request, data=None):
    form = Convert_data(request.POST)
    if data is None and form.is_valid():
        data = form.cleaned_data
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
            "Status": HttpResponse.status_code,
            "data": {
                "currency": data['currency'],
                'time': data['time'],
                'result': "%.2f" % res_data
            }
        }
        return JsonResponse(ctx)
    return HttpResponse("There's no value or currency")
