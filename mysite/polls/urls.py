from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.EditView.as_view(), name='edit'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/vote/', views.VoteView.as_view(), name='vote'),
    # path('', views.index, name='index'),
    # path('<int:question_id>/<int:q_id>/<str:quest_id>/', views.detail, name='detail'),
]
