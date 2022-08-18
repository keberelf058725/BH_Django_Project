import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas
import numpy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import auth
from datetime import datetime, timedelta
from .forms import Flash_File_Form, Clinical_DC_Form, Vivitrol_Form
import json
from django.templatetags.static import static
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from .graphs import return_graph_LOC, return_graph_AGE, return_graph_gender, return_graph_DOC
from requests import post
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import Nurse, Admin, Flash_User, Therapist

pandas.options.mode.chained_assignment = None

# production
#census_path = '/home/beachhouse/PycharmProjects/BH_Django_Project/BH_DJANGO/Static_File_Storage/census_info_beachhouse.csv'
#flash_path = '/home/beachhouse/PycharmProjects/BH_Django_Project/BH_DJANGO/Static_File_Storage/Flash_Changes.csv'


# development
census_path = static('census_info_beachhouse.csv')
flash_path = static('Flash_Changes.csv')


def logout_user(request):
    auth.logout(request)
    return redirect('login')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            nurse = form.cleaned_data['Nurse']
            therapist = form.cleaned_data['Therapist']
            admin = form.cleaned_data['Admin']
            flash_user = form.cleaned_data['Flash_User']

            nurse_model = Nurse()
            nurse_model.user = user
            nurse_model.Nurse = nurse

            therapist_model = Therapist()
            therapist_model.user = user
            therapist_model.Therapist = therapist

            admin_model = Admin()
            admin_model.user = user
            admin_model.Admin = admin

            flash_model = Flash_User()
            flash_model.user = user
            flash_model.Flash_User = flash_user

            nurse_model.save()
            therapist_model.save()
            admin_model.save()
            flash_model.save()
            form.save()

            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register_user.html", context={"register_form": form})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '192.168.201.185',
                        'site_name': 'Beach House Analytics',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'kevincaldon@beachhousecenter.com', [user.email], fail_silently=True)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


@login_required
def viv_help_view(request, *args, **kwargs):
    return render(request, "viv_help.html", {})


@login_required
def homepage_view(request, *args, **kwargs):
    if request.method == 'POST':

        if 'recent_ad' in request.POST:
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="recentadmits.csv"'},
            )

            t = datetime.today() - timedelta(days=3)
            df = pandas.read_csv(census_path)
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
            new_admissions.to_csv(path_or_buf=response, float_format='%.4f', index=False, decimal=".")

            return response

        if 'caseload' in request.POST:
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="Caseload.csv"'},
            )
            df2_dl = pandas.read_csv(census_path)
            df2_dl[['Therapist', 'trash']] = df2_dl.primarycareteam_primarytherapist.str.split(' ', n=1, expand=True)
            df2_dl['Therapist'] = df2_dl['Therapist'].replace(['Did'], 'No Assigned Therapist')
            df2_dl['LNF3'] = df2_dl['last_name'].str.slice(stop=3)
            df2_dl['Name'] = df2_dl.loc[:, 'first_name'] + ' ' + df2_dl.loc[:, 'LNF3']
            df2_dl['program_name'] = df2_dl['program_name'].replace(['2 Detox'], 'DTX')
            df2_dl['program_name'] = df2_dl['program_name'].replace(['4 Residential'], 'RES')
            df2_dl['program_name'] = df2_dl['program_name'].replace(['5 PHP'], 'PHP')
            df2_dl['program_name'] = df2_dl['program_name'].replace(['6 IOP 5 Days'], 'IOP')
            df2_dl = df2_dl[['Therapist', 'Name', 'mr', 'program_name']]
            df2_dl.rename(columns={"mr": "MRN", "program_name": "Level of Care"})
            df2_dl = df2_dl.sort_values("Therapist")
            df2_dl.to_csv(path_or_buf=response, float_format='%.4f', index=False, decimal=".")

            return response

    if request.method == 'GET':
        t = datetime.today() - timedelta(days=3)
        df = pandas.read_csv(census_path)
        df2 = pandas.read_csv(census_path)
        df2[['Therapist', 'trash']] = df2.primarycareteam_primarytherapist.str.split(' ', n=1, expand=True)
        df2['Therapist'] = df2['Therapist'].replace(['Did'], 'No Assigned Therapist')
        df2 = df2[['Therapist']]
        df2 = df2.value_counts().rename_axis('Therapist').reset_index(name='Count_of_Patients')
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
        json_records2 = df2.reset_index().to_json(orient='records')

        data = json.loads(json_records)
        data2 = json.loads(json_records2)
        context = {'d': data, 'd2': data2}

        context['chart_LOC'] = return_graph_LOC()
        context['chart_G'] = return_graph_gender()
        context['chart_Age'] = return_graph_AGE()
        context['chart_DOC'] = return_graph_DOC()

    return render(request, "home.html", context)


@login_required
@permission_required('pages.view_nurse', raise_exception=True)
def viv_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = Vivitrol_Form(request.POST, request.FILES)
        if form.is_valid():
            try:
                sheet1 = request.FILES['Viv_File']
                Viv = pandas.DataFrame(pandas.read_csv(sheet1))
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
                messages.error(request, 'Unknown Columns Detected: Operation Cancelled')
            else:
                messages.success(request,
                                 'The total number of Vivitrol Injections from {} to {} is: {}'.format(Date_Min,
                                                                                                       Date_Max,
                                                                                                       VivT))

            return render(request, "viv.html", {})
    else:
        form = Vivitrol_Form()

    return render(request, "viv.html", {'form': form})


@login_required
def flash_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = Flash_File_Form(request.POST, request.FILES)

        if form.is_valid():
            try:
                flash_1 = request.FILES['Flash_File']
                flash_2 = request.FILES['Kipu_File']

                Actual_Flash = pandas.DataFrame(pandas.read_excel(flash_1, header=None))
                DL_Flash = pandas.DataFrame(pandas.read_csv(flash_2))
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
                    ['Name', 'MR', 'Sex', 'Insurance 1   Insurance Company', 'Admission Date', 'Length Of Stay',
                     'Program',
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

            except Exception:
                messages.error(request, 'Unknown Columns Detected: Operation Cancelled')
            else:
                json_records = M_D.reset_index().to_json(orient='records')
                data = json.loads(json_records)
                context = {'d': data}

                return render(request, 'flash_return.html', context)

    else:
        form = Flash_File_Form()

    return render(request, 'flash.html', {'form': form})


@login_required
def clinical_dc_view(request, *args, **kwargs):
    if request.method == 'POST':

        if 'cl_analyze' in request.POST:

            form = Clinical_DC_Form(request.POST, request.FILES)

            if form.is_valid():
                try:
                    ALOS_File = request.FILES['ALOS_File']
                    DC_File = request.FILES['DC_File']
                    M_S = request.POST['Start_Date']
                    M_E = request.POST['End_Date']
                    T_L = request.FILES['Therapist']
                    # inclusive
                    Month_Start = pandas.to_datetime(M_S)
                    # exclusive
                    Month_End = pandas.to_datetime(M_E)
                    # Read LOS file
                    ALOS = pandas.DataFrame(pandas.read_csv(ALOS_File))
                    # Read DC File
                    DC = pandas.DataFrame(pandas.read_csv(DC_File))
                    # Change DC Date to Date/Time
                    DC.loc[:, ('Discharge Date')] = pandas.to_datetime(DC.loc[:, ('Discharge Date')])
                    # Filter Rows to April DCs
                    DC2 = DC[(DC['Discharge Date'] >= Month_Start) & (DC['Discharge Date'] < Month_End)]
                    # Replace ADMIN DC TYPES
                    DC2['Discharge Type'] = DC2['Discharge Type'].replace(
                        ['ADMINISTRATIVE – NO SHOW', "ADMINISTRATIVE – BEHAVIORAL ", "ADMINISTRATIVE – BEHAVIORAL",
                         'ADMINISTRATIVE – LEGAL'], 'ADMIN DC')
                    # REPLACE DETOX/STAB ONLY TYPES
                    DC2['Discharge Type'] = DC2['Discharge Type'].replace(['DETOX COMPLETE', 'STABILIZATION ONLY'],
                                                                          'DETOX/STAB ONLY')
                    # DROP ALL PRE-ADMISSION RECORDS
                    DC3 = DC2[DC2['Discharge Type'].str.contains('PRE-ADMISSION') == False]
                    # Grab only needed Columns
                    ALOS1 = ALOS[
                        ['MR#', 'Admission Date', 'Discharge Date', 'Detox Actual', 'Residential Actual',
                         'PHP/Day-Night Actual',
                         'IOP Actual', 'IIP Actual', 'PHP/Day-Night Treatment with Community Housing Actual',
                         'Length of Stay']]
                    # drop rows with null values
                    ALOS2 = ALOS1.dropna()
                    # Change DC Date to Date/Time
                    ALOS2.loc[:, ('Discharge Date')] = pandas.to_datetime(ALOS2['Discharge Date'])
                    # Verify D/T
                    # ALOS2.info()
                    # Filter Rows to April DCs
                    ALOS3 = ALOS2[(ALOS2['Discharge Date'] >= Month_Start) & (ALOS2['Discharge Date'] < Month_End)]
                    ALOS4 = ALOS3.rename(columns={'Length of Stay': 'UR LOS'})
                    # Merge Both Files
                    MRG = pandas.merge(DC3, ALOS4, how="left", left_on=["MR"], right_on=["MR#"], suffixes=("", ".ALOS"))
                    # Create STAGE 1 LOS
                    MRG['Stage 1 LOS'] = MRG.loc[:, ['Detox Actual', 'Residential Actual', 'IIP Actual']].sum(axis=1)
                    # SUM PHP COLUMNS
                    MRG['PHP Actual'] = MRG.loc[:,
                                        ['PHP/Day-Night Actual',
                                         'PHP/Day-Night Treatment with Community Housing Actual']].sum(
                        axis=1)
                    # CREATE STAGE 2 COLUMNS
                    MRG['Stage 2 LOS'] = MRG.loc[:, ['PHP Actual', 'IOP Actual']].sum(axis=1)
                    # CREATE TOTAL LOS COLUMN
                    MRG['TOTAL LOS'] = MRG.loc[:, ['Stage 1 LOS', 'Stage 2 LOS']].sum(axis=1)
                    MRG['Stage 2 Conversion'] = numpy.where(MRG['Stage 2 LOS'] > 0, 'Converted', 'Unconverted')
                    MRG['PHP Conversion'] = numpy.where(MRG['PHP Actual'] > 0, 'Converted', 'Unconverted')
                    MRG['IOP Actual'] = pandas.to_numeric(MRG['IOP Actual'])
                    MRG['IOP Conversion'] = numpy.where(MRG['IOP Actual'] > 0, 'Converted', 'Unconverted')
                    MRG['Stage 1 to PHP Conversion'] = numpy.where((MRG['Stage 1 LOS'] > 0) & (MRG['PHP Actual'] > 0),
                                                                   'Converted',
                                                                   'Unconverted')
                    MRG['HELPER'] = MRG.loc[:, ['Stage 1 LOS', 'PHP Actual']].sum(axis=1)
                    MRG['Stage 1 to IOP Conversion'] = numpy.where((MRG['IOP Actual'] > 0) & (MRG['HELPER'] > 0),
                                                                   'Converted',
                                                                   'Unconverted')
                    MRG['PHP into IOP Conversion'] = numpy.where((MRG['IOP Actual'] > 0) & (MRG['PHP Actual'] > 0),
                                                                 'Converted',
                                                                 'Unconverted')
                    MRG[['Statuses_1', 'Statuses_2']] = MRG.Statuses.str.split(';', n=1, expand=True)
                    MRG['Stage_1_Therapist'] = numpy.where(MRG.loc[:, ('Statuses_2')].str.contains("Campus Therapist"),
                                                           MRG.loc[:, ('Statuses_2')], MRG.loc[:, ('Statuses_1')])
                    MRG[['Stage_1_Therapist_1', 'Stage_1_Therapist_2']] = MRG.Stage_1_Therapist.str.split(': ', n=1,
                                                                                                          expand=True)
                    MRG[['Stage_1', 'Stage_1_Therapist_4']] = MRG.Stage_1_Therapist_2.str.split(',', n=1, expand=True)
                    MRG[['Stage_2', 'Stage_2_Eronious']] = MRG['Primary Therapist'].str.split(',', n=1, expand=True)
                    MRG['DCDATE_COPY'] = MRG['Discharge Date'].astype(str)
                    MRG[['DCYEAR', 'DCM', 'DCD']] = MRG.DCDATE_COPY.str.split('-', expand=True)
                    MRG['DCYT'] = MRG['DCYEAR'].str.slice(start=2)
                    MRG['DC_Month'] = MRG.loc[:, ('DCM')].astype(str) + MRG.loc[:, ('DCYT')].astype(str)
                    MRG['Admit_Yr'] = MRG.loc[:, ('DCYEAR')]
                    MRG['Admit_Yr_Filter'] = MRG.loc[:, ('DCYEAR')]
                    MRG['RELAPSE'] = numpy.where(
                        (MRG['PHP Actual'] > 0) & ((MRG['Program'].str.contains("4 - Residential")) | (
                            MRG['Program'].str.contains("4 - Residential"))), "True", "False")
                    MRG['Include_on_Campus1'] = numpy.where(MRG['Stage 2 Conversion'].str.contains("Unconverted"), "Y",
                                                            "N")
                    MRG['Include_on_Campus'] = numpy.where(MRG['RELAPSE'].str.contains("True"), "Y",
                                                           MRG.loc[:, ('Include_on_Campus1')])
                    MRG1 = MRG[
                        ['First Name', 'Last Name', 'MR', 'Insurance 1   Insurance Company', 'Discharge Type',
                         'Admission Date',
                         'Discharge Date', 'DC_Month', 'Length Of Stay', 'Detox Actual', 'IIP Actual',
                         'Residential Actual',
                         'Stage 1 LOS', 'PHP Actual', 'IOP Actual', 'Stage 2 LOS', 'TOTAL LOS', 'Stage 2 Conversion',
                         'PHP Conversion', 'IOP Conversion', 'Stage 1 to PHP Conversion', 'Stage 1 to IOP Conversion',
                         'PHP into IOP Conversion', 'UR LOS', 'Stage_1', 'Stage_2', 'Program', 'Payment Method',
                         'Admit_Yr',
                         'Admit_Yr_Filter', 'RELAPSE', 'Include_on_Campus']]
                    TR = pandas.DataFrame(pandas.read_excel(T_L))
                    MRG2 = pandas.merge(MRG1, TR, how="left", left_on=["Stage_1"], right_on=["Full Name"],
                                        suffixes=("", "_TR"))
                    MRG3 = pandas.merge(MRG2, TR, how="left", left_on=["Stage_2"], right_on=["Full Name"],
                                        suffixes=("", "_TR"))
                    MRG3.rename(columns={'Therapist': 'S1 Therapist', 'Therapist_TR': 'S2 Therapist'}, inplace=True)
                    MRG3[['S1 Therapist', 'S2 Therapist']] = MRG3[['S1 Therapist', 'S2 Therapist']].fillna(
                        'Former Employee')
                    Final_Preped_Data = MRG3[
                        ['First Name', 'Last Name', 'MR', 'Insurance 1   Insurance Company', 'Discharge Type',
                         'Admission Date',
                         'Discharge Date', 'DC_Month', 'Length Of Stay', 'Detox Actual', 'IIP Actual',
                         'Residential Actual',
                         'Stage 1 LOS', 'PHP Actual', 'IOP Actual', 'Stage 2 LOS', 'TOTAL LOS', 'Stage 2 Conversion',
                         'PHP Conversion', 'IOP Conversion', 'Stage 1 to PHP Conversion', 'Stage 1 to IOP Conversion',
                         'PHP into IOP Conversion', 'UR LOS', 'S1 Therapist', 'S2 Therapist', 'Program',
                         'Payment Method',
                         'Admit_Yr', 'Admit_Yr_Filter', 'RELAPSE', 'Include_on_Campus']]
                except Exception:
                    messages.error(request, 'Unknown Columns Detected: Operation Cancelled')

                else:
                    context = Final_Preped_Data.to_pickle("./df.pkl")

                return render(request, 'cl_dc_dl.html', context)
            else:
                messages.error(request, 'One or more fields contained errors')

        if 'cl_dl' in request.POST:
            df = pandas.read_pickle("./df.pkl")

            LM = (pandas.Period(datetime.now(), 'M') - 1).strftime('%B')

            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="' + LM + '".csv"'},
            )

            df.to_csv(path_or_buf=response, float_format='%.4f', index=False, decimal=".")

            return response

    else:
        form = Clinical_DC_Form()

    return render(request, 'clinical.html', {'form': form})


@login_required
def cl_dc_dl_view(request, *args, **kwargs):
    return render(request, 'cl_dc_dl.html', {})


@login_required
def flash_report_tools_view(request, *args, **kwargs):
    if request.method == 'POST':
        if 'report_refresh' in request.POST:
            requests.post(
                'https://prod-176.westus.logic.azure.com:443/workflows/ea291131ff8a4a2f919d0f854a31a4ec/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=E68W4i4IA8AWzu4TSyBaxcVZipma60B5Nd_lUGGVbVg')

        if 'fl_changes' in request.POST:
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="yesterday_census_changes.csv"'},
            )

            df = pandas.read_csv(flash_path)

            df.to_csv(path_or_buf=response, float_format='%.4f', index=False, decimal=".")

            return response

        return render(request, 'flash_tools.html', {})

    if request.method == 'GET':
        df = pandas.read_csv(flash_path)
        df = df[['Patient', 'Change', 'LOC_Change', 'Commit_LOS']]
        json_records = df.reset_index().to_json(orient='records')
        # data = []
        data = json.loads(json_records)
        context = {'d': data}

    return render(request, 'flash_tools.html', context)
