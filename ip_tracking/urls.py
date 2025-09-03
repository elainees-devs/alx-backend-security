from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),      # POST login
    path('graphql/', views.graphql_view, name='graphql') # POST GraphQL
]
