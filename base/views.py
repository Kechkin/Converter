import base64
import json
from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from base.forms import *
from base.service import *


def check_permissions(perm):
    def wrapped(func):
        def inner(request, *args):
            if request.user.is_active:
                perm_list = request.user.get_user_permissions()
                if perm in perm_list:
                    return func(request, *args)
            raise PermissionDenied

        return inner

    return wrapped


def check_user(func):
    def wrapped(request, *args):
        if request.user.is_authenticated:
            return func(request, *args)
        else:
            if 'HTTP_AUTHORIZATION' in request.META:
                user_data = request.META['HTTP_AUTHORIZATION'].split()
                username, password = (base64.b64decode(user_data[1])).decode().split(":")
                user = authenticate(username=username, password=password)
                if user is not None:
                    return func(request)
        return HttpResponse('Unauthenticated', status=401)

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
        "add": AddData(),
        "search": SearchData(),
        "convert": ConvertData()
    }
    return render(request, "base/index.html", context)


@check_http(['POST'])
@check_user
@check_permissions('base.add_exchangerate')
def api_add(request):
    data = json.loads(request.body)
    form = AddData(data)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({"Data": form.cleaned_data})
        except Exception as e:
            return JsonResponse({"Error": e})
    return JsonResponse({"Error": form.cleaned_data})


@check_http(['POST'])
@check_user
@check_permissions('base.view_exchangerate')
def api_search(request):
    data_json = json.loads(request.body)
    form = SearchData(data_json)
    if form.is_valid():
        try:
            data = form.cleaned_data
            ctx = search(data)
            return JsonResponse(ctx)
        except Exception as e:
            return JsonResponse({"Error": e})
    return JsonResponse({"Error": form.cleaned_data})


@check_user
@check_http(['POST'])
@check_permissions('base.add_exchangerate')
def api_convert(request):
    data_json = json.loads(request.body)
    form = ConvertData(data_json)
    if form.is_valid():
        try:
            data = form.cleaned_data
            ctx = convert(data)
            return JsonResponse(ctx)
        except Exception as e:
            return JsonResponse({"Error": e})
    return JsonResponse({"Error": form.cleaned_data})


@check_user
@check_http(["POST", "GET"])
@check_permissions('base.add_exchangerate')
def add_ui(request):
    form = AddData(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        form = AddData(request.POST)
    return render(request, 'base/add.html', {'form': form})


@check_user
@check_http(["POST", "GET"])
@check_permissions('base.view_exchangerate')
def search_ui(request):
    form = SearchData(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        context = search(data)
        return render(request, "base/search.html", {"context": context})
    else:
        form = SearchData(request.POST)
    return render(request, 'base/search.html', {'form': form})


@check_user
@check_http(["POST"])
@check_permissions('base.add_exchangerate')
def convert_ui(request):
    form = ConvertData(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        ctx = convert(data)
        return render(request, "base/convert.html", {"context": ctx})
    else:
        form = ConvertData(request.POST)
    return render(request, "base/convert.html", {"form": form})
