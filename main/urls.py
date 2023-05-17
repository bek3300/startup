from django.urls import path
from .import  views
from django.urls import path,re_path

from . import views2

app_name = 'main'
urlpatterns = [
    path('',views2.homePage, name='homepage'),
    path('login/',views2.loginUser, name='login'),
    path('currentUserConnectUserList/',views2.currentUserConnectUserList, name='currentUserConnectUserList'),
    path('home/',views2.logged_user, name='home'),
    path('messages/',views2.messages, name='messages'),
    path('message_detail/',views2.message_detail, name='message_detail'),

    path('logout/',views2.logout_view, name='logout'),
    path('explore/',views2.explore, name='explore'),
    path('profile/',views2.profile, name='profile'),
    path('register/',views2.register, name='register'),
    path('networks/<str:typeOf>',views2.networks, name='networks'),
    path('connect/',views2.connect, name='connect'),
    path('connect-list/',views2.connect_list, name='connect_list'),
    path('users/<int:pk>/', views2.connect_list_view, name='connect_list_view'),
    path('users/', views2.users_list, name='users_list'),
    path('filter/<str:typeOf>', views2.filter, name='filter'),
    path('get-content/<str:typeOf>', views2.getContent, name='get_content'),
    re_path(r'^users/cancel/(?P<id>[\w-]+)/$', views2.cancel_friend_request),
    re_path(r'^users/accept/(?P<id>[\w-]+)/$', views2.accept_friend_request),
    re_path(r'^users/delete/(?P<id>[\w-]+)/$', views2.delete_friend_request),
    path('users/send/<int:id>/', views2.send_friend_request, name='freind_request'),



    path('admin/',views2.admin, name='admin'),
#     path('<int:pk>/', views.BookDetailView.as_view(), name='detail'),
]

# urlpatterns=[
#      path('',views.homePage, name='homepage'),
#      path('active-partners/',views.activePartner, name='active_partner'),
#      path('register-users/',views.registerUsers, name='user-registration'),
#      path('networks/',views.networkStartups, name='networks'),

#      path('logout/',views.logout_view, name='logout'),
#      path('profile/',views.profile, name='profile'),
#      path('password/', views.change_password, name='change_password'),




# ]