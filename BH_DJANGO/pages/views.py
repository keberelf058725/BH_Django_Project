from django.http import HttpResponse
from django.shortcuts import render


def homepage_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def viv_view(request, *args, **kwargs):
    return render(request, "viv.html", {})

"""if request.method == 'POST' and 'submit' in request.POST:
    
    from vivitrol_script import import_csv_data
    
    import_csv_data()
    
    return HttpResponseRedirect(reverse(app_name:view_name))"""