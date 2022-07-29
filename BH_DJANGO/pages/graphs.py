import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from io import StringIO
import pandas
import numpy
from django.templatetags.static import static

bgcolor = '#E6E6E6'
lbcolor = '#000000'


def return_graph_LOC():
    plt.rcParams['figure.figsize'] = (5, 3)

    fig, ax = plt.subplots(facecolor=bgcolor)

    # pandas func
    df = pandas.read_csv(static('census_info_beachhouse.csv'))
    df['program_name'] = df['program_name'].replace(['2 Detox'], 'DTX')
    df['program_name'] = df['program_name'].replace(['4 Residential'], 'RES')
    df['program_name'] = df['program_name'].replace(['5 PHP Day Night Treatment with Community Hou'], 'PHP')
    df['program_name'] = df['program_name'].replace(['6 IOP 5 Days'], 'IOP')
    df = df[['program_name']]
    df = df.value_counts().rename_axis('Level of Care').reset_index(name='Count of Patients')
    df['colors'] = numpy.where(df['Level of Care'] == 'DTX', 'lightcoral',
                               numpy.where(df['Level of Care'] == 'RES', 'cornflowerblue',
                                           numpy.where(df['Level of Care'] == 'PHP', 'gold',
                                                       numpy.where(df['Level of Care'] == 'IOP', 'blueviolet',
                                                                   'black'))))
    df['sort_key'] = numpy.where(df['Level of Care'] == 'DTX', 1,
                                 numpy.where(df['Level of Care'] == 'RES', 2,
                                             numpy.where(df['Level of Care'] == 'PHP', 3,
                                                         numpy.where(df['Level of Care'] == 'IOP', 4,
                                                                     5))))
    df = df.sort_values('sort_key').reset_index(drop=True)

    # Values for PLot
    c = df['colors']
    x = df['Level of Care']
    y = df['Count of Patients']

    # Bar PLot
    bars = plt.bar(x, height=y, width=0.8, bottom=None, align='center', data=None, color=c)
    # ['purple', 'blue', 'red']
    # Axis Forming
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(lbcolor)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=lbcolor)
    ax.xaxis.grid(False)

    # Grab the color of the bars so we can make the
    # text the same color.
    bar_color = bars[1].get_facecolor()

    # Add text annotations to the top of the bars.
    # Note, you'll have to adjust this slightly (the 0.3)
    # with different data.
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            round(bar.get_height(), 1),
            horizontalalignment='center',
            color=lbcolor,
            weight='bold'
        )

    # Add labels and a title. Note the use of `labelpad` and `pad` to add some
    # extra space between the text and the tick labels.
    ax.set_xlabel('Level of Care', labelpad=15, color=lbcolor, backgroundcolor=bgcolor)
    ax.set_ylabel('Patient Count', labelpad=15, color=lbcolor, backgroundcolor=bgcolor)
    ax.set_title('Patients by Level of Care', pad=15, color=lbcolor,
                 weight='bold', backgroundcolor=bgcolor)
    ax.margins(0)
    ax.set_facecolor(color=bgcolor)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def return_graph_gender():
    plt.rcParams['figure.figsize'] = (5, 3)

    fig, ax = plt.subplots(facecolor=bgcolor)

    # pandas func
    df = pandas.read_csv(static('census_info_beachhouse.csv'))
    df = df[['sex']]
    df = df.value_counts().rename_axis('Gender').reset_index(name='Count of Patients')

    # Values for PLot
    x = df['Gender']
    y = df['Count of Patients']
    explode = (1, 0)

    # Pie PLot
    bars = plt.pie(y, labels=x, colors=['blue', 'pink'], autopct='%1.1f%%',
                   shadow=True, startangle=90)

    # Axis Forming
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(lbcolor)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=lbcolor)
    ax.xaxis.grid(False)

    ax.set_title('Patients by Gender', pad=15, color=lbcolor,
                 weight='bold', backgroundcolor=bgcolor)

    ax.set_facecolor(color=lbcolor)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def return_graph_AGE():
    plt.rcParams['figure.figsize'] = (12, 5)

    fig, ax = plt.subplots(facecolor=bgcolor)

    # pandas func
    df = pandas.read_csv(static('census_info_beachhouse.csv'))
    df = df[['age']]
    df['age_groups'] = numpy.where(df['age'] <= 25, '18-25',
                                   numpy.where((df['age'] > 25) & (df['age'] <= 35), '26-35',
                                               numpy.where((df['age'] > 35) & (df['age'] <= 49), '36-49',
                                                           numpy.where(df['age'] >= 50, '50+', ''))))
    df = df[['age_groups']]
    df = df.value_counts().rename_axis('Age Groups').reset_index(name='Count of Patients')
    df['colors'] = numpy.where(df['Age Groups'] == '18-25', 'lightskyblue',
                               numpy.where(df['Age Groups'] == '26-35', 'whitesmoke',
                                           numpy.where(df['Age Groups'] == '36-49', 'lightsalmon',
                                                       numpy.where(df['Age Groups'] == '50+', 'lightgrey', 'black'))))
    df['srt_key'] = numpy.where(df['Age Groups'] == '18-25', 1,
                                numpy.where(df['Age Groups'] == '26-35', 2,
                                            numpy.where(df['Age Groups'] == '36-49', 3,
                                                        numpy.where(df['Age Groups'] == '50+', 4, 5))))
    df = df.sort_values('srt_key').reset_index(drop=True)

    # Values for PLot
    c = df['colors']
    x = df['Age Groups']
    y = df['Count of Patients']

    # Bar PLot
    bars = plt.bar(x, height=y, width=0.8, bottom=None, align='center', data=None, color=c)
    # ['purple', 'blue', 'red']
    # Axis Forming
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(lbcolor)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=lbcolor)
    ax.xaxis.grid(False)

    # Grab the color of the bars so we can make the
    # text the same color.
    bar_color = bars[1].get_facecolor()

    # Add text annotations to the top of the bars.
    # Note, you'll have to adjust this slightly (the 0.3)
    # with different data.
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            round(bar.get_height(), 1),
            horizontalalignment='center',
            color=lbcolor,
            weight='bold'
        )

    # Add labels and a title. Note the use of `labelpad` and `pad` to add some
    # extra space between the text and the tick labels.
    ax.set_xlabel('Age Groups', labelpad=15, color=lbcolor, backgroundcolor=bgcolor)
    ax.set_ylabel('Patient Count', labelpad=15, color=lbcolor, backgroundcolor=bgcolor)
    ax.set_title('Patients by Age Groups', pad=15, color=lbcolor,
                 weight='bold', backgroundcolor=bgcolor)
    ax.margins(0)
    ax.set_facecolor(color=bgcolor)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


