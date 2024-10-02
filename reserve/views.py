from django.shortcuts import render

def homeReserve(request):
    return render(request, 'reserve/home_reserve.html', {'name_page': 'homeReserve'})


def homePage(request):
    return render(request, 'reserve/home_page.html', {'name_page': 'home'})