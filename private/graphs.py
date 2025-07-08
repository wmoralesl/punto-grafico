# from .models import Client, Order
import locale
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from config.settings import S_LOCALE


locale.setlocale(locale.LC_TIME, S_LOCALE)

def lastTwelveMonths(Object, option, currentDate):
    monthsCount = [0] * 12
    twelveMonthsAgo = currentDate-relativedelta(months=11)

    if (option == "clientes"):
        for i in range(12):
            date = twelveMonthsAgo + relativedelta(months=i)
            monthsCount[i] = Object.objects.filter(Q(created__year=date.year) & Q(created__month=date.month)).count()

    if (option == "orders"):
        for i in range(12):
            date = twelveMonthsAgo + relativedelta(months=i)
            monthsCount[i] = Object.objects.filter(Q(request_date__year=date.year) & Q(request_date__month=date.month)).count()

    return monthsCount

def lastTwelveMonthsName(currentDate):
    monthsName = [""] * 12
    twelveMonthsAgo = currentDate-relativedelta(months=11)

    for i in range(12):
        date = twelveMonthsAgo + relativedelta(months=i)
        monthsName[i] = f"{date.strftime('%b')}{date.strftime('%y')}"
    return monthsName


