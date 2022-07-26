from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas
import numpy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import auth
from datetime import datetime, timedelta
from .forms import Flash_File_Form
import json
from django.templatetags.static import static
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from .dum_graph_func import return_graph


def logout_user(request):
    auth.logout(request)
    return redirect('login')


@login_required
def viv_help_view(request, *args, **kwargs):
    return render(request, "viv_help.html", {})


@login_required
def homepage_view(request, *args, **kwargs):
    if request.method == 'GET':
        t = datetime.today() - timedelta(days=3)
        df = pandas.read_csv(static('census_info_beachhouse.csv'))
        df[['Therapist', 'trash']] = df.primarycareteam_primarytherapist.str.split(' ', n=1, expand=True)
        df[['DOC', 'trash.1']] = df.diagcodename_list.str.split(' ', n=1, expand=True)
        df['LNF3'] = df['last_name'].str.slice(stop=3)
        df['Name'] = df.loc[:, 'first_name'] + ' ' + df.loc[:, 'LNF3']
        df = df[['Name', 'mr', 'admission_date', 'program_name', 'length_of_stay', 'age', 'sex', 'DOC', 'Therapist',
                 'paymentmethod']]
        df['Therapist'] = df['Therapist'].replace(['Did'], 'No Assigned Therapist')
        df['program_name'] = df['program_name'].replace(['2 Detox'], 'DTX')
        df['program_name'] = df['program_name'].replace(['4 Residential'], 'RES')
        df['program_name'] = df['program_name'].replace(['5 PHP'], 'PHP')
        df['program_name'] = df['program_name'].replace(['6 IOP 5 Days'], 'IOP')
        df['admission_date_1'] = df['admission_date']
        df.loc[:, ('admission_date_1')] = pandas.to_datetime(df.loc[:, ('admission_date_1')])
        new_admissions = df[(df['admission_date_1'] >= t)].sort_values(by='admission_date_1', ascending=False)
        new_admissions[['admission_date', 'trash.2']] = df.admission_date.str.split(' ', n=1, expand=True)
        new_admissions[['Y', 'M', 'D']] = new_admissions.admission_date.str.split('-', n=2, expand=True)
        new_admissions['admission_date'] = new_admissions.loc[:, ('M')] + "-" + new_admissions.loc[:,
                                                                                ('D')] + "-" + new_admissions.loc[:,
                                                                                               ('Y')]
        new_admissions = new_admissions[
            ['Name', 'mr', 'admission_date', 'program_name', 'length_of_stay', 'age', 'sex', 'DOC', 'Therapist',
             'paymentmethod']]
        json_records = new_admissions.reset_index().to_json(orient='records')
        # data = []
        data = json.loads(json_records)
        context = {'d': data}
        # context = {'d': data, 'chart': chart}
        context['chart'] = return_graph()

        #context = {'d': data, 'chart': chart}

    return render(request, "home.html", context)


@login_required
@permission_required('pages.view_nurse', raise_exception=True)
def viv_view(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, "viv.html", {})

    if request.method == 'POST':
        try:
            sheet1 = request.FILES['file']
            Viv = pandas.DataFrame(pandas.read_csv(sheet1, dtype=str))
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
            messages.success(request,
                             'The total number of Vivitrol Injections from {} to {} is: {}'.format(Date_Min, Date_Max,
                                                                                                   VivT))

        return render(request, "viv.html", {})
    else:
        return render(request, "viv.html", {})


def flash_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = Flash_File_Form(request.POST)
        print(request.FILES)

        # if form.is_valid():

        try:
            flash_1 = request.FILES['Flash_File']
            flash_2 = request.FILES['Kipu_File']
        except Exception:
            messages.error(request, 'Wrong File Type')
        else:
            Actual_Flash = pandas.DataFrame(pandas.read_excel(flash_1, header=None))
            DL_Flash = pandas.DataFrame(pandas.read_csv(flash_2, dtype=str))
            Actual_Flash['Patient'] = Actual_Flash[0]
            Actual_Flash['MRN'] = Actual_Flash[1]
            Actual_Flash = Actual_Flash[['Patient', 'MRN']]
            Actual_Flash = Actual_Flash.dropna()
            Actual_Flash = Actual_Flash[Actual_Flash['Patient'].str.contains('Name') == False]
            Actual_Flash = Actual_Flash[Actual_Flash['Patient'].str.contains('ON CAMPUS') == False]
            Actual_Flash = Actual_Flash[Actual_Flash['Patient'].str.contains('OFF CAMPUS') == False]
            Actual_Flash = Actual_Flash[Actual_Flash['Patient'].str.contains('Residential') == False]
            Actual_Flash = Actual_Flash.reset_index()
            Actual_Flash = Actual_Flash[['Patient', 'MRN']]
            DL_Flash['LNF3'] = DL_Flash['Last Name'].str.slice(stop=3)
            DL_Flash['LNF2'] = DL_Flash['Last Name'].str.slice(stop=2)
            DL_Flash['Name_3'] = DL_Flash.loc[:, 'First Name'] + ' ' + DL_Flash.loc[:, 'LNF3']
            DL_Flash['Name_2'] = DL_Flash.loc[:, 'First Name'] + ' ' + DL_Flash.loc[:, 'LNF2']
            DL_Flash['Name'] = DL_Flash.loc[:, 'First Name'] + ' ' + DL_Flash.loc[:, 'Last Name']
            DL_Flash = DL_Flash[
                ['Name', 'MR', 'Sex', 'Insurance 1   Insurance Company', 'Admission Date', 'Length Of Stay', 'Program',
                 'Payment Method', 'LNF3', 'LNF2', 'Name_3', 'Name_2']]
            M_D = pandas.merge(DL_Flash, Actual_Flash, how="left", left_on=["Name_3"], right_on=["Patient"],
                               suffixes=("", ".Flash"))
            M_D = pandas.merge(M_D, Actual_Flash, how="left", left_on=["Name_2"], right_on=["Patient"],
                               suffixes=("", ".Match2"))
            M_D = pandas.merge(M_D, Actual_Flash, how="left", left_on=["MR"], right_on=["MRN"],
                               suffixes=("", ".MRN_MATCH"))
            M_D['Boolean'] = numpy.where(
                (M_D['Patient'].isnull()) & (M_D['Patient.Match2'].isnull()) & (M_D['Patient.MRN_MATCH'].isnull()),
                True, False)
            M_D = M_D[M_D['Boolean'] == True]
            M_D = M_D.rename(columns={'Insurance 1   Insurance Company': 'Insurance', 'Admission Date': 'Admission',
                                      'Length Of Stay': 'LOS', 'Payment Method': 'Payment'})
            M_D = M_D[['Name', 'MR', 'Sex', 'Insurance', 'Admission', 'LOS', 'Program', 'Payment']]
            json_records = M_D.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}

            return render(request, 'flash_return.html', context)

    # except Exception:
    # messages.error(request, 'Unexpected Error: Possibility that no file was selected')
    # else:
    # messages.success(request,
    # 'Patient is '.format(M_D))
    # return render(request, "flash.html", {})
    else:
        form = Flash_File_Form()

    return render(request, 'flash.html', {'form': form})
