from matplotlib import pyplot as plt
from io import StringIO
import pandas
from django.templatetags.static import static
from IPython.display import set_matplotlib_formats


def return_graph():
    set_matplotlib_formats('retina', quality=100)

    plt.rcParams['figure.figsize'] = (8, 5)

    fig, ax = plt.subplots()

    # pandas func
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
    df = df[['program_name']]
    df = df.value_counts().rename_axis('Level of Care').reset_index(name='Count of Patients')

    # Values for PLot
    x = df['Level of Care']
    y = df['Count of Patients']

    # Bar PLot
    bars = plt.bar(x, height=y, width=0.8, bottom=None, align='center', data=None)

    # Axis Forming
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    # Grab the color of the bars so we can make the
    # text the same color.
    bar_color = bars[0].get_facecolor()

    # Add text annotations to the top of the bars.
    # Note, you'll have to adjust this slightly (the 0.3)
    # with different data.
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            round(bar.get_height(), 1),
            horizontalalignment='center',
            color=bar_color,
            weight='bold'
        )

    # Add labels and a title. Note the use of `labelpad` and `pad` to add some
    # extra space between the text and the tick labels.
    ax.set_xlabel('Level of Care', labelpad=15, color='#333333')
    ax.set_ylabel('Patient Count', labelpad=15, color='#333333')
    ax.set_title('Patient Count by Level of Care', pad=15, color='#333333',
                 weight='bold')

    fig.tight_layout()

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data
