from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#from django.template import loader

from .models import Ipv4, Ipv6, Zakaznici

#@login_required
#def index(request):
#    latest_zakaznici_list = Zakaznici.objects.order_by('-id')[:5]
#    context = {'latest_zakaznici_list': latest_zakaznici_list}
#    return render(request, 'isp/index.html', context)
#
#def detail(request, zakaznici_id):
#    zakaznik = get_object_or_404(Zakaznici, pk=zakaznici_id)
#    return render(request, 'zakaznici/detail.html', {'zakaznik': zakaznik})
#
#def results(request, zakaznici_id):
#    zakaznik = get_object_or_404(Zakaznici, pk=zakaznici_id)
#    return render(request, 'zakaznici/results.html', {'zakaznik': zakaznik})


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'isp/index.html'
    context_object_name = 'zakaznici_list'

    def get_queryset(self):
        """Vraci seznam zakazniku."""
        #return Zakaznici.objects.order_by('-id')[:5]
        return Zakaznici.objects.all()


@method_decorator(login_required, name='dispatch')
class DetailView(generic.DetailView):
    model = Zakaznici
    template_name = 'isp/detail.html'


@method_decorator(login_required, name='dispatch')
class ZakaznikVloz(generic.CreateView):
    model = Zakaznici
    fields = ['prijmeni','jmeno','telefon','email']
    template_name = 'isp/zakaznik_vloz.html'
    success_url = reverse_lazy('isp:index')


@method_decorator(login_required, name='dispatch')
class ZakaznikEdit(generic.UpdateView):
    model = Zakaznici
    fields = ['prijmeni','jmeno','telefon','email']
    template_name = 'isp/zakaznik_editace.html'
    success_url = reverse_lazy('isp:index')
    #nebo navrat na sebe samo
    #success_url = "."
    #def get_context_data(self, **kwargs):
    #    context = super(ZakaznikEdit, self).get_context_data(**kwargs)
    #    context['ipv4_adresy'] = Ipv4.objects.all() #whatever you would like
    #    return context


@method_decorator(login_required, name='dispatch')
class ZakaznikSmaz(generic.DeleteView):
    model = Zakaznici
    success_url = reverse_lazy('isp:index')


@method_decorator(login_required, name='dispatch')
class ResultsView(generic.DetailView):
    model = Zakaznici
    template_name = 'isp/results.html'


#TODO jen testovaci
@login_required
def vote(request, zakaznici_id):
    zakaznici = get_object_or_404(Zakaznici, pk=zakaznici_id)
    try:
        selected_ipv4 = zakaznici.ipv4_set.get(pk=request.POST['ipv4'])
    except (KeyError, Ipv4.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'isp/detail.html', {
            'zakaznici': zakaznici,
            'error_message': "You didn't select an IPv4.",
        })
    else:
        selected_ipv4.votes += 1
        selected_ipv4.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('isp:results', args=(zakaznici.id,)))


@method_decorator(login_required, name='dispatch')
class Ipv4Vloz(generic.CreateView):
    model = Ipv4
    fields = ['ip_adresa','aktivni']
    template_name = 'isp/ipv4_vloz.html'
    #TODO
    #success_url = reverse_lazy('isp:zakaznik_edit', args=self.kwargs.get('zakaznici_id'))

    #je potřeba přepsat metodu, aby jsme ziskali cizi klic id_zakaznika
    def form_valid(self, form):
        #form.instance.id_zakaznika = get_object_or_404(Zakaznici, id=self.kwargs.get('zakaznici_id'))
        #tady je rozumnejsi chyba
        form.instance.id_zakaznika = Zakaznici.objects.get(id=self.kwargs.get('zakaznici_id'))
        return super(Ipv4Vloz, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.kwargs['zakaznici_id']})


@method_decorator(login_required, name='dispatch')
class Ipv4Edit(generic.UpdateView):
    model = Ipv4
    fields = ['ip_adresa','aktivni']
    template_name = 'isp/ipv4_editace.html'
    #success_url = reverse_lazy('isp:zakaznik_edit', kwargs={'id':model.id_zakaznika})

    #def get_initial(self):
    #    return {
    #        'ip_adresa': "10.0.0.138",
    #    }

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.object.id_zakaznika.id})


@method_decorator(login_required, name='dispatch')
class Ipv4Smaz(generic.DeleteView):
    model = Ipv4

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.object.id_zakaznika.id})


@method_decorator(login_required, name='dispatch')
class Ipv6Vloz(generic.CreateView):
    model = Ipv6
    fields = ['prefix','maska','aktivni']
    template_name = 'isp/ipv6_vloz.html'

    #TODO vyresit kontrolu vlozenych dat, at nam sedi IP a maska
    #napr. viz: https://stackoverflow.com/questions/29981690/django-form-validation-on-class-based-view
    #ale asi to neni pro tento projekt zasadni

    #je potřeba přepsat metodu, aby jsme ziskali cizi klic id_zakaznika
    def form_valid(self, form):
        form.instance.id_zakaznika = Zakaznici.objects.get(id=self.kwargs.get('zakaznici_id'))
        return super(Ipv6Vloz, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.kwargs['zakaznici_id']})


@method_decorator(login_required, name='dispatch')
class Ipv6Edit(generic.UpdateView):
    model = Ipv6
    fields = ['prefix','maska','aktivni']
    template_name = 'isp/ipv6_editace.html'

    #TODO viz Ipv6Vloz

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.object.id_zakaznika.id})


@method_decorator(login_required, name='dispatch')
class Ipv6Smaz(generic.DeleteView):
    model = Ipv6

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.object.id_zakaznika.id})
