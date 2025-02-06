from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('Aindex/', Aindex, name='Aindex'),
    path('home/', home, name='home'),
    path('profile/', profile, name='profile'),
    path('logout/',signout, name='logout'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('update_profile/', update_profile, name='update_profile'),
    path('create_post/', create_post, name='create_post'),
    path('signout/', signout, name='signout'),
    path('Aregistration/', Aregistration, name='Aregistration'),
    path('Aregistration1/', Aregistration1, name='Aregistration1'),
    path('aprofile/',Aprofile, name='Aprofile'),
    path('update_Aprofile/',update_Aprofile, name='update_Aprofile'), 
    path('Ahome/', Ahome, name='Ahome'),
    path('add_person/', add_person, name='add_person'),
    path('register/', register, name='register'),
    path('Track/<str:order_id>/',Track, name='Track'),
    path('view-shipment/<str:order_id>/',ViewShipmentDetails, name='ViewShipmentDetails'),
]
