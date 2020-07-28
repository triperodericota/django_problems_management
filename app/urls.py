from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('problem/', views.ProblemCreateView.as_view(), name='problem-create'),
    path('problem/<int:pk>/update', views.ProblemUpdateView.as_view(), name='problem-update'),
    path('problem/<int:pk>/delete', views.ProblemDeleteView.as_view(), name='problem-delete'),
    path('problem/<int:pk>/detail', views.ProblemDetailView.as_view(), name='detail'),
    path('find/tag/<tag_name>', views.FindByTagView.as_view(), name='find_by_tag'),
    path('find/difficulty/<difficulty_name>', views.FindByDifficultyView.as_view(), name='find_by_difficulty'),
    path('search/', views.SearchByNameView.as_view(), name='search_by_name')
]
