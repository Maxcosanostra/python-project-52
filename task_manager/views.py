from django.shortcuts import render


def index(request):
    return render(request, "index.html")


# def rollbar_test(request):
#     """
#     Тест rollbar на вызов AttributeError
#     """
#     a = None
#     a.hello()  # тут сознательная ошибка
#     return render(request, "index.html")
