from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from openhireapi.models import Profile
from django.contrib.auth.models import User

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
        fields = ('id', 'url', 'user', 'city', 'state', 'linkedin', 'github', 'resume', 'portfolio', 'codingchallenge')
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

        profile = Profile.objects.get(pk=pk)

        profile.city = request.data["city"]
        profile.state = request.data["state"]
        profile.linkedin = request.data["linkedin"]
        profile.github = request.data["github"]
        profile.resume = request.data["resume"]
        profile.portfolio = request.data["portfolio"]
        profile.codingchallenge = request.data["codingchallenge"]

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
            # user = User.objects.get(pk=request.data["user_id"])

            profile = Profile.objects.get(pk=pk)

            profile.city = None
            profile.state = None
            profile.linkedin = None
            profile.github = None
            profile.resume = None
            profile.portfolio = None
            profile.codingchallenge = None

            # user.first_name = request.data["first_name"]
            # user.last_name = request.data["last_name"]

            # user.save()

            # profile.user = user

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
        # profiles = profiles.filter(linkedin__isnull=False, github__isnull=False, resume__isnull=False, portfolio__isnull=False, codingchallenge__isnull=False)

        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request})
        return Response(serializer.data)