from itertools import chain
from django.shortcuts import render
from AcaLoc.models import *
from django.db.models import Q
import openrouteservice as ors
import folium
import geocoder


def about(request):
    return render(request, 'AcaLoc/about.html', {})

def showmap(request):
    return render(request, 'AcaLoc/map.html', {})



def deneme(request, *args, **kwargs):
    obj = Academician.objects.all()
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


# def home(request, *args, **kwargs):
# words = request.GET.get('q', '').split(" ")
# a_filters = Q()
# d_filters = Q()
# s_filters = Q()
#
# for word in words:
#     a_filters |= Q(name__icontains=word) | Q(last_name__icontains=word)
#     d_filters |= Q(name__icontains=word)
#     s_filters |= Q(name__icontains=word) | Q(tag__icontains=word)
#     Aca = Academican.objects.filter(a_filters)
#     Dep = Department.objects.filter(d_filters)
#     Market = MarketPlace.objects.filter(d_filters)
#     Sop = Shops.objects.filter(s_filters)
#     query_chain = list(chain(
#         Aca,
#         Dep,
#         Market,
#         Sop
#     ))
# if words[0] == '':
#     cont = {
#
#     }
#     return render(request, 'AcaLoc/home.html', {'cont': cont})
# return render(request, 'AcaLoc/home.html', {'query_chain': query_chain})

def home(request):
    ors_key = "5b3ce3597851110001cf624868767a25d6ad4aafb8da4295bbd1cb19"
    # performs requests to the ORS API services
    # client will be used in all examples
    client = ors.Client(key=ors_key)

    words = request.GET.get('q','').split(" ")

    a_filters = Q()
    d_filters = Q()
    s_filters = Q()


    for word in words:
        hasempty = 1
        context = {}
        a_filters |= Q(name__icontains=word) | Q(last_name__icontains=word)
        #d_filters |= Q(name__icontains=word)
        s_filters |= Q(name__icontains=word) | Q(tag__icontains=word)
        Aca = Academician.objects.filter(a_filters)
        Build = Buildings.objects.filter(s_filters)
        Sop = Shops.objects.filter(s_filters)

        query_chain = list(chain(
            Aca,
            Build,
            Sop
        ))
        context['query_chain'] = query_chain

        if words[0] == '':
            context['hasempty'] = hasempty
            print(hasempty, "If statement")
            return render(request, 'AcaLoc/home.html', context)

        liste = []

        for i in query_chain:
            print(query_chain)
            try:
                liste.append(i.longitude)
                liste.append(i.latitude)
            except:
                liste.append(i.buildings.longitude)
                liste.append(i.buildings.latitude)
        #print(liste)

        myloc = geocoder.ip('me')
        lonlat = myloc
        coordinates = [liste,[myloc.lng,myloc.lat]]
        # directions
        route = client.directions(coordinates=coordinates,
                                  profile='foot-walking',
                                  format='geojson')
        # map
        map_directions = folium.Map(location=[39.86643210602186, 32.73390451366158], zoom_start=15)

        # add geojson to map
        folium.GeoJson(route, name='route').add_to(map_directions)

        # add layer control to map (allows layer to be turned on or off)
        folium.LayerControl().add_to(map_directions)

        # display map
        map_directions.save("AcaLoc/templates/AcaLoc/map.html")
        liste = []


        hasempty = 0
        context['hasempty'] = hasempty
        print(hasempty, "out of if statement")

        return render(request, 'AcaLoc/home.html', context)
