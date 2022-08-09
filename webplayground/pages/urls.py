from django.urls import path
from .views import PageListView, PageDetailView, PageCreate, PageUpdate, PageDelete

# urls_de_pages es un nombre cualquiera. Este será configurado en el urls.py global
urls_de_pages = ([
    # rutas de vistas basadas en funciones:
    # path('', views.pages, name='pages'),
    # path('<int:page_id>/<slug:page_slug>/', views.page, name='page'),

    # rutas de vistas basadas en clases:
    path('', PageListView.as_view(), name='pages'),
    path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),

    path('create/', PageCreate.as_view(), name='create'),
    path('update/<int:pk>/', PageUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PageDelete.as_view(), name='delete'),
], 'pages')