from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import pandas
import numpy
import datetime


def homepage_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def viv_view(request, *args, **kwargs):


    if request.method == 'GET':
        return render(request, "viv.html", {})

    if request.method == 'POST':
        try:
            sheet1 = request.FILES['file']
            Viv = pandas.DataFrame(pandas.read_csv(sheet1, index_col=0, dtype=str))
            Viv[['Evaluation Date', 'Evaluation Date_2']] = Viv['Evaluation Date'].str.split(' ', n=1, expand=True)
            Viv.loc[:, ('Evaluation Date')] = pandas.to_datetime(Viv.loc[:, ('Evaluation Date')]).dt.date
            Date_Min = Viv['Evaluation Date'].min()
            Date_Max = Viv['Evaluation Date'].max()
            Date_Min = Date_Min.strftime('%b %d %Y')
            Date_Max = Date_Max.strftime('%b %d %Y')
            Viv['Count'] = 1
            VivT = numpy.sum(Viv['Count'])
            VivT = str(VivT)
        except Exception:
            messages.error(request, 'Unexpected Error: Possibility that no file was selected')
        else:
            messages.success(request, 'The total number of Vivitrol Injections from {} to {} is: {}'.format(Date_Min, Date_Max, VivT))

        return render(request, "viv.html", {})
    else:
        return render(request, "viv.html", {})


