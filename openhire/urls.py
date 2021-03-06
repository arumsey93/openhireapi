from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from openhireapi.models import *
from openhireapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'profiles', Profiles, 'profile')
router.register(r'jobs', Jobs, 'job')
router.register(r'favorites', Favorites, 'favorite')
router.register(r'users', Users, 'user')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
