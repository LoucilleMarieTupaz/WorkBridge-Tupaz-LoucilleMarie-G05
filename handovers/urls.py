from django.urls import path
from . import views


app_name = 'handovers'


urlpatterns = [
    path('', views.handover_list, name='list'),

    path('create/', views.handover_create, name='create'),

    path('<int:pk>/', views.handover_detail, name='detail'),

    path('<int:pk>/edit/', views.handover_update, name='update'),

    path('<int:pk>/delete/', views.handover_delete, name='delete'),
]
