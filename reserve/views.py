from django.shortcuts import render
from companion.models import Companion


def homeReserve(request):
    companions = Companion.objects.all()
    return render(
        request,
        "reserve/home_reserve.html",
        {"name_page": "homeReserve", "companions": companions},
    )


def homePage(request):
    return render(request, "reserve/home_page.html", {"name_page": "home"})
