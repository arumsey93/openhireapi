from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from openhireapi.models import Profile
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.db.models import Q

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for profile
    Arguments:
        serializers
    """
    class Meta:
        model = Profile
        url = serializers.HyperlinkedIdentityField(
            view_name='profile',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'city', 'state', 'linkedin', 'github', 'resume', 'portfolio', 'codingchallenge', 'techOne', 'techTwo', 'techThree')
        depth=1


class Profiles(ViewSet):
    """Profiles for Open.HIRE"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Profile instance
        """
        new_profile = Profile()
        new_profile.city = request.data["city"]
        new_profile.state = request.data["state"]
        new_profile.linkedin = request.data["linkedin"]
        new_profile.github = request.data["github"]
        new_profile.resume = request.data["resume"]
        new_profile.portfolio = request.data["portfolio"]
        new_profile.codingchallenge = request.data["codingchallenge"]
        new_profile.techOne = request.data["techOne"]
        new_profile.techTwo = request.data["techTwo"]
        new_profile.techThree = request.data["techThree"]

        user = Profile.objects.get(user=request.auth.user)
        new_profile.save()

        serializer = ProfileSerializer(new_profile, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for profile
        Returns:
            Response -- JSON serialized profile instance
        """
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a profile
        Returns:
            Response -- Empty body with 204 status code
        """

        user = User.objects.get(pk=request.data["user_id"])

        profile = Profile.objects.get(user=request.user)

        profile.city = request.data["city"]
        profile.state = request.data["state"]
        profile.linkedin = request.data["linkedin"]
        profile.github = request.data["github"]
        profile.resume = request.data["resume"]
        profile.portfolio = request.data["portfolio"]
        profile.codingchallenge = request.data["codingchallenge"]
        profile.techOne = request.data["techOne"]
        profile.techTwo = request.data["techTwo"]
        profile.techThree = request.data["techThree"]

        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]

        user.save()

        profile.user = user

        profile.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single profile
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:

            profile = Profile.objects.get(pk=pk)

            profile.city = None
            profile.state = None
            profile.linkedin = None
            profile.github = None
            profile.resume = None
            profile.portfolio = None
            profile.codingchallenge = None
            profile.techOne = None
            profile.techTwo = None
            profile.techThree = None

            profile.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Profile.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to profile
        Returns:
            Response -- JSON serialized list of profiles
        """
        profiles = Profile.objects.all()

        city = self.request.query_params.get('city', None)
        state = self.request.query_params.get('state', None)
        tech = self.request.query_params.get('tech', None)

        if city is not None:
            profiles = profiles.filter(city=city)

        if state is not None:
            profiles = profiles.filter(state=state)

        if tech is not None:
            profiles = profiles.filter(Q(techOne__startswith=tech)|Q(techTwo__startswith=tech)|Q(techThree__startswith=tech))

        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def current_profile(self, request):
        """Special action to get current user without having to know/send the user id from client"""

        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(
            profile,
            context={'request': request}
        )
        return Response(serializer.data)