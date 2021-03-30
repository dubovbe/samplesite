from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('rubrics', APIRubricViewSet)


urlpatterns = [
    path('', index, name='index'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', user_register_activate, name='user_register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/password/change/', ChangeUserPasswordView.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),

    path('api/', include(router.urls)),
    # path('api/rubrics/', api_rubrics),
    path('api/rubrics/', APIRubrics.as_view()),
    path('api/bbs/', APIBbs.as_view()),
    path('api/bbs/<int:rubric_id>/', api_bbs_by_rubric),
    # path('api/bbs/<int:rubric_id>/', APIBBsByRubric.as_view()),
    # path('api/bb/<int:pk>/', api_bb_detail),
    path('api/bb/<int:pk>/', APIBbDetail.as_view()),

]
