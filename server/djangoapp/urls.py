from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    # path for about view
    path(route='about/',view=views.about,name='about'),
    # path for contact us view
    path(route='contact/',view=views.contact,name='contact'),
    # path for registration
    path('registration/', views.registration_request, name='registration'),
    # path for login
    path('login/', views.login_request, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),
    # path(route='', view=views.get_dealerships, name='index'),
    path(route='', view=views.get_dealerships, name='index'),
    # path for dealer reviews view
    # this could be an incorrect path--> path(route='dealer_details/<int:id>/', view=views.get_dealer_details, name='dealer_details'),
    # not sure if this is the correct one --> path(route='dealer/<int:id>/', view=views.get_dealer_details, name='dealer_details'),
    # path for dealer_details view
    path('dealer/<int:id>/', views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    #path('dealer/<int:id>/review', views.add_review, name='add_review'),
    path(route='dealer/<int:id>/add-review/', view=views.add_review, name="add_review")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)