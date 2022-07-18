import numpy

def import_csv_data():
    csv_file_path = askopenfilename()
    Viv = pandas.read_csv(csv_file_path)
    Viv[['Evaluation Date', 'Evaluation Date_2']] = Viv['Evaluation Date'].str.split(' ', n=1, expand=True)
    Viv.loc[:, ('Evaluation Date')] = pandas.to_datetime(Viv.loc[:, ('Evaluation Date')]).dt.date
    Date_Min = Viv['Evaluation Date'].min()
    Date_Max = Viv['Evaluation Date'].max()
    Viv['Count'] = 1
    VivT = numpy.sum(Viv['Count'])