from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', user_register_activate, name='user_register_activate'),
    path('accounts/register/done', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/password/change/', ChangeUserPasswordView.as_view(), name='password_change'),
    path('accounts/profile/delete', DeleteUserView.as_view(), name='profile_delete'),

]
