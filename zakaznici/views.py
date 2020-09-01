from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

#from django.template import loader

from .models import Ipv4, Zakaznici


#def index(request):
#    latest_zakaznici_list = Zakaznici.objects.order_by('-id')[:5]
#    context = {'latest_zakaznici_list': latest_zakaznici_list}
#    return render(request, 'zakaznici/index.html', context)
#
#def detail(request, zakaznici_id):
#    zakaznik = get_object_or_404(Zakaznici, pk=zakaznici_id)
#    return render(request, 'zakaznici/detail.html', {'zakaznik': zakaznik})
#
#def results(request, zakaznici_id):
#    zakaznik = get_object_or_404(Zakaznici, pk=zakaznici_id)
#    return render(request, 'zakaznici/results.html', {'zakaznik': zakaznik})

class IndexView(generic.ListView):
    template_name = 'zakaznici/index.html'
    context_object_name = 'latest_zakaznici_list'

    def get_queryset(self):
        """Return the last five zakaznici."""
        return Zakaznici.objects.order_by('-id')[:5]


class DetailView(generic.DetailView):
    model = Zakaznici
    template_name = 'zakaznici/detail.html'


class ResultsView(generic.DetailView):
    model = Zakaznici
    template_name = 'zakaznici/results.html'


#TODO jen testovaci
def vote(request, zakaznici_id):
    zakaznici = get_object_or_404(Zakaznici, pk=zakaznici_id)
    try:
        selected_ipv4 = zakaznici.ipv4_set.get(pk=request.POST['ipv4'])
    except (KeyError, Ipv4.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'zakaznici/detail.html', {
            'zakaznici': zakaznici,
            'error_message': "You didn't select an IPv4.",
        })
    else:
        selected_ipv4.votes += 1
        selected_ipv4.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('zakaznici:results', args=(zakaznici.id,)))