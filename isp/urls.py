from django.urls import path

from . import views

app_name = 'isp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('', views.index, name='index'),
    #path('<int:zakaznici_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:zakaznici_id>/vote/', views.vote, name='vote'),
]
