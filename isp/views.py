from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

#from django.template import loader

from .models import Ipv4, Ipv6, Zakaznici, TarifniSkupiny, Tarify, Adresy

#from .forms import ZakaznikEditForm

@method_decorator(login_required, name='dispatch')
class IndexView(generic.TemplateView):
    template_name = 'isp/index.html'
    pocet_Z = Zakaznici.objects.count()
    pocet_IP4 = Ipv4.objects.count()
    pocet_IP6 = Ipv6.objects.count()
    pocet_TS = TarifniSkupiny.objects.count()
    pocet_T = Tarify.objects.count()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'pocet_Z': self.pocet_Z,
            'pocet_IP4': self.pocet_IP4,
            'pocet_IP6': self.pocet_IP6,
            'pocet_TS': self.pocet_TS,
            'pocet_T': self.pocet_T,
            })
        return context


@method_decorator(login_required, name='dispatch')
class ZakazniciView(generic.ListView):
    template_name = 'isp/zakaznici.html'
    context_object_name = 'zakaznici_list'

    def get_queryset(self):
        """Vraci seznam zakazniku."""
        #return Zakaznici.objects.order_by('-id')[:5]
        return Zakaznici.objects.all()


@method_decorator(login_required, name='dispatch')
class ZakaznikVloz(generic.CreateView):
    model = Zakaznici
    fields = ['prijmeni','jmeno','telefon','email']
    template_name = 'isp/generic_vloz.html'
    success_url = reverse_lazy('isp:zakaznici')


@method_decorator(login_required, name='dispatch')
class ZakaznikEdit(generic.UpdateView):
    model = Zakaznici
    fields = ['prijmeni','jmeno','telefon','email','id_adresy','id_tarifu']
    #form_class = ZakaznikEditForm
    template_name = 'isp/zakaznik_editace.html'
    success_url = reverse_lazy('isp:zakaznici')

    #pro poslani promenne do forms
    #def get_form_kwargs(self, **kwargs):
    #    form_kwargs = super(ZakaznikEdit, self).get_form_kwargs(**kwargs)
    #    form_kwargs["id_tarifniskupiny"] = self.object.id_adresy.id_tarifniskupiny
    #    return form_kwargs

    #lepsi vyber tarifu by se asi musel resit pres JS
    tarify = Tarify.objects.all()
    def get_context_data(self, **kwargs):
        context = super(ZakaznikEdit, self).get_context_data(**kwargs)
        context.update({
            'tarify': self.tarify,
            })
        return context

    #kontrola vyberu tarifu ze spravne skupiny podle adresy
    def form_valid(self, form):
        #kdyz neni vybran tarif, neni co kontrolovat
        if (form['id_tarifu'].value()==''):
            #form['id_tarifu'].value=None
            return super(ZakaznikEdit, self).form_valid(form)
        #kdyz neni vybrana adresa, taky neni co kontrolovat, ale zaroven zneplatnime nastaveni tarifu
        elif (form['id_adresy'].value()==''):
            #form['id_adresy'].value=None
            #form['id_tarifu'].value=None
            form.instance.id_tarifu=None
            return super(ZakaznikEdit, self).form_valid(form)
        #jinak zkontrolovat jestli k sobe sedi
        else:
            adresa=Adresy.objects.filter(id=form['id_adresy'].value())[0]
            tarif=Tarify.objects.filter(id=form['id_tarifu'].value())[0]
            #pokud id tarifni skupiny neodpovida dle vybraneho tarifu vs. dle adresy
            if (tarif.id_tarifniskupiny.id != adresa.id_tarifniskupiny.id):
                form.add_error('id_tarifu', 'Na dané adrese není takový tarif k dispozici, volte z tarifní skupiny "%s"!' % adresa.id_tarifniskupiny.nazev)
                return super(ZakaznikEdit, self).form_invalid(form)
            else:
                return super(ZakaznikEdit, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ZakaznikSmaz(generic.DeleteView):
    model = Zakaznici
    template_name = 'isp/generic_confirm_delete.html'
    success_url = reverse_lazy('isp:zakaznici')


@method_decorator(login_required, name='dispatch')
class Ipv4Vloz(generic.CreateView):
    model = Ipv4
    fields = ['ip_adresa','aktivni']
    template_name = 'isp/generic_vloz.html'

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
    template_name = 'isp/generic_editace.html'

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.object.id_zakaznika.id})


@method_decorator(login_required, name='dispatch')
class Ipv4Smaz(generic.DeleteView):
    model = Ipv4
    template_name = 'isp/generic_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.object.id_zakaznika.id})


@method_decorator(login_required, name='dispatch')
class Ipv6Vloz(generic.CreateView):
    model = Ipv6
    fields = ['prefix','maska','aktivni']
    template_name = 'isp/generic_vloz.html'

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
    template_name = 'isp/generic_editace.html'

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.object.id_zakaznika.id})


@method_decorator(login_required, name='dispatch')
class Ipv6Smaz(generic.DeleteView):
    model = Ipv6
    template_name = 'isp/generic_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('isp:zakaznik_edit', kwargs={'pk': self.object.id_zakaznika.id})


@method_decorator(login_required, name='dispatch')
class TarifniSkupinyView(generic.ListView):
    template_name = 'isp/tarifni_skupiny.html'
    context_object_name = 'tarifni_skupiny_list'

    def get_queryset(self):
        """Vraci seznam tarifnich skupin."""
        return TarifniSkupiny.objects.all()


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required("isp.add_tarifniskupiny",raise_exception=False), name="dispatch")
class TarifniSkupinaVloz(generic.CreateView):
    model = TarifniSkupiny
    fields = ['nazev']
    template_name = 'isp/generic_vloz.html'
    #success_url = reverse_lazy('isp:tarifni_skupiny')

    #editace teto nove skupiny
    def get_success_url(self):
        return reverse_lazy('isp:tarifni_skupina_edit', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required("isp.delete_tarifniskupiny",raise_exception=False), name="dispatch")
class TarifniSkupinaSmaz(generic.DeleteView):
    model = TarifniSkupiny
    template_name = 'isp/generic_confirm_delete.html'
    success_url = reverse_lazy('isp:tarifni_skupiny')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required("isp.change_tarifniskupiny",raise_exception=False), name="dispatch")
class TarifniSkupinaEdit(generic.UpdateView):
    model = TarifniSkupiny
    fields = ['nazev']
    template_name = 'isp/tarifni_skupina_detail.html'
    success_url = "."

    #vratit zpet samo na sebe - slozitejsi varianta
    #def get_success_url(self):
    #    return reverse_lazy('isp:tarifni_skupina_edit', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required("isp.add_tarify",raise_exception=False), name="dispatch")
class TarifVloz(generic.CreateView):
    model = Tarify
    fields = ['nazev','cena','rychlost_down','rychlost_up']
    template_name = 'isp/generic_vloz.html'
    #success_url = reverse_lazy('isp:tarifni_skupiny')

    #je potřeba přepsat metodu, aby jsme ziskali cizi klic id_zakaznika
    def form_valid(self, form):
        #chybejici polozka formulare podle models.py - z promenne z urls.py
        form.instance.id_tarifniskupiny = TarifniSkupiny.objects.get(id=self.kwargs.get('ts_id'))
        return super(TarifVloz, self).form_valid(form)

    #vratit na tarifni skupinu
    def get_success_url(self):
        return reverse_lazy('isp:tarifni_skupina_edit', kwargs={'pk': self.kwargs['ts_id']})


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required("isp.change_tarify",raise_exception=False), name="dispatch")
class TarifEdit(generic.UpdateView):
    model = Tarify
    fields = ['nazev','cena','rychlost_down','rychlost_up']
    template_name = 'isp/generic_editace.html'
    #success_url = reverse_lazy('isp:tarifni_skupiny')

    #vratit na tarifni skupinu
    def get_success_url(self):
        return reverse_lazy('isp:tarifni_skupina_edit', kwargs={'pk': self.kwargs['ts_id']})


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required("isp.delete_tarify",raise_exception=False), name="dispatch")
class TarifSmaz(generic.DeleteView):
    model = Tarify
    template_name = 'isp/generic_confirm_delete.html'
    #success_url = reverse_lazy('isp:tarifni_skupiny')

    #vratit na tarifni skupinu
    def get_success_url(self):
        return reverse_lazy('isp:tarifni_skupina_edit', kwargs={'pk': self.kwargs['ts_id']})
