from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Users
    Arguments:
        serializers
    """
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field = 'id'
        )
        fields = ('id', 'url', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'date_joined')
        depth = 1


class Users(ViewSet):
    """Users for Open.HIRE
    Purpose: Allow a user to communicate with the Open.HIRE database to GET PUT POST and DELETE Users.
    Methods: GET PUT(id) POST
"""


    def retrieve(self, request, pk=None):
        """Handle GET requests for single profile
        Purpose: Allow a user to communicate with the Open.HIRE database to retrieve  one user
        Methods:  GET
        Returns:
            Response -- JSON serialized profile instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



    def list(self, request):
        """Handle GET requests to profiles resource
        Purpose: Allow a user to communicate with the Open.HIRE database to retrieve list of users
        Methods:  GET
        Returns:
            Response -- JSON serialized list of users
        """
        users = Users.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)