from django.urls import path,re_path
from moviesapp import views

urlpatterns = [
    path('movies/', views.MoviesList.as_view(),name='post_movie'), 
    path('movies/<int:id>/', views.MovieDetail.as_view(),name='get_movie'),  
    path('ratings/', views.RatingsView.as_view(),name='create_rating'), 
]