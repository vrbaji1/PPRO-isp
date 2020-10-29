from django.urls import path

from . import views

app_name = 'isp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('', views.index, name='index'),

    #path('<int:zakaznici_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    path('zakaznik_vloz/', views.ZakaznikVloz.as_view(), name='zakaznik_vloz'),
    path('zakaznik_edit_<int:pk>/', views.ZakaznikEdit.as_view(), name='zakaznik_edit'),
    path('zakaznik_smaz_<int:pk>/', views.ZakaznikSmaz.as_view(), name='zakaznik_smaz'),

    path('ipv4_vloz_<int:zakaznici_id>/', views.Ipv4Vloz.as_view(), name='ipv4_vloz'),
    path('ipv4_edit_<int:pk>/', views.Ipv4Edit.as_view(), name='ipv4_edit'),
    path('ipv4_smaz_<int:pk>/', views.Ipv4Smaz.as_view(), name='ipv4_smaz'),

    path('ipv6_vloz_<int:zakaznici_id>/', views.Ipv6Vloz.as_view(), name='ipv6_vloz'),
    path('ipv6_edit_<int:pk>/', views.Ipv6Edit.as_view(), name='ipv6_edit'),
    path('ipv6_smaz_<int:pk>/', views.Ipv6Smaz.as_view(), name='ipv6_smaz'),

    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:zakaznici_id>/vote/', views.vote, name='vote'),

    path('tarifni_skupiny/', views.TarifniSkupinyView.as_view(), name='tarifni_skupiny'),
    path('tarifni_skupina_vloz/', views.TarifniSkupinaVloz.as_view(), name='tarifni_skupina_vloz'),
    path('tarifni_skupina_edit_<int:pk>/', views.TarifniSkupinaEdit.as_view(), name='tarifni_skupina_edit'),
    path('tarifni_skupina_smaz_<int:pk>/', views.TarifniSkupinaSmaz.as_view(), name='tarifni_skupina_smaz'),
    #path('tarifni_skupina_detail_<int:pk>/', views.TarifniSkupinaDetail.as_view(), name='tarifni_skupina_detail'),

    path('tarifni_skupina_<int:ts_id>/tarif_vloz/', views.TarifVloz.as_view(), name='tarif_vloz'),
    path('tarifni_skupina_<int:ts_id>/tarif_edit_<int:pk>/', views.TarifEdit.as_view(), name='tarif_edit'),
    path('tarifni_skupina_<int:ts_id>/tarif_smaz_<int:pk>/', views.TarifSmaz.as_view(), name='tarif_smaz'),
]
