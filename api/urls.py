from django.urls import path

from api import views

urlpatterns = [
    path('articles/<int:cat_id>/', views.ArticleApiView.as_view()),
    path('home/', views.HomeApiView.as_view()),
    path('queries/<int:cat_id>/', views.QueriesApiView.as_view()),
    path('create_article/', views.ArticleCreateApiView.as_view()),
    path('estimate/', views.GradeApiView.as_view()),
]
