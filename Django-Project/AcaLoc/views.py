from itertools import chain
from django.shortcuts import render
from AcaLoc.models import *
from django.db.models import Q


def about(request):
    return render(request, 'AcaLoc/about.html', {'title': 'Malumço'})


def deneme(request, *args, **kwargs):
    obj = Academican.objects.all()
    context = {
        "object": obj,
    }
    return render(request, 'AcaLoc/deneme.html', context)


"""
def autosuggest(request):
    q_filters = Q()
    query_original = request.GET.get("term")
    q_filters |= Q(name__icontains=query_original) | Q(last_name__icontains=query_original)
    queryset = Academican.objects.filter(q_filters)
    myList = []
    myList += [x.name for x in queryset]
    return JsonResponse(myList,safe=False)
"""


def home(request, *args, **kwargs):
    words = request.GET.get('q', '').split(" ")
    a_filters = Q()
    d_filters = Q()
    s_filters = Q()

    for word in words:
        a_filters |= Q(name__icontains=word) | Q(last_name__icontains=word)
        d_filters |= Q(name__icontains=word)
        s_filters |= Q(name__icontains=word) | Q(tag__icontains=word)
        Aca = Academican.objects.filter(a_filters)
        Dep = Department.objects.filter(d_filters)
        Market = MarketPlace.objects.filter(d_filters)
        Sop = Shops.objects.filter(s_filters)
        query_chain = list(chain(
            Aca,
            Dep,
            Market,
            Sop
        ))

    if words[0] == '':
        cont = {

        }
        return render(request, 'AcaLoc/home.html', {'cont': cont})
    return render(request, 'AcaLoc/home.html', {'query_chain': query_chain})
