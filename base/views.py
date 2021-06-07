import base64
from datetime import datetime
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from base.forms import *


def check_user(func):
    def wrapped(request):
        if request.user.is_authenticated and 'HTTP_AUTHORIZATION' in request.META:
            user_data = request.META['HTTP_AUTHORIZATION'].split()
            username, password = (base64.b64decode(user_data[1])).decode().split(":")
            user = User.objects.get(username=username)
            if user.is_active:
                return func(request)
        return HttpResponse('Unauthorized', status=401)
    return wrapped


def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, "base/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, "base/login.html", {"form": form})


@check_user
def index(request):
    context = {
        "add": Add_data(),
        "search": Search_data(),
        "convert": Convert_data()
    }

    return render(request, "base/index.html", context)


@check_user
def add(request):
    if request.method == "POST":
        form = Add_data(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return HttpResponse("Error")


@check_user
def search(request):
    if request.method == "POST":
        form = Search_data(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if not data['time']:
                data['time'] = datetime.today()
            result = Exchange_rate.objects.get_data(data['time'], data['currency'])
            for i in result:
                context = {
                    "currency": data['currency'],
                    "time": i.pub_time,
                    "value": i.value
                }
                return JsonResponse(context)
    return HttpResponse("There's no value or currency")


@check_user
def convert(request):
    if request.method == "POST":
        form = Convert_data(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if not data['time']:
                data['time'] = datetime.today()
            value1, value2 = None, None

            result = Exchange_rate.objects.filter(pub_time__lte=data['time'], currency=data['currency'])[:1].values(
                'value')
            for item in result:
                value1 = item['value']

            result2 = Exchange_rate.objects.filter(pub_time__lte=data['time'], currency=data['currency2'])[:1].values(
                'value')

            for item in result2:
                value2 = item['value']

            res_data = (data['money'] * value1) / value2
            ctx = {
                "currency": data['currency'],
                'time': data['time'],
                'result': "%.2f" % res_data
            }
            return JsonResponse(ctx)
    return HttpResponse("There's no value or currency")