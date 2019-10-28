from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from openhireapi.models import Profile, Job, Favorite
from .profile import ProfileSerializer
from .job import JobSerializer

class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for favorites
    Arguments:
        serializers
    """
    product = ProfileSerializer(many=False)
    class Meta:
        model = Favorite
        url = serializers.HyperlinkedIdentityField(
            view_name='favorite',
            lookup_field='id'
        )
        fields = ('id', 'url', 'profile', 'job')
        depth = 2

class Favorites(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized favorite instance
        """
        new_favorite = Favorite()
        new_favorite.job = Job.objects.get(pk=request.data["job"])
        new_favorite.profile = Profile.objects.get(user=request.auth.user)

        new_favorite.save()

        serializer = FavoriteSerializer(new_favorite, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single favorite
        Returns:
            Response -- JSON serialized favorite instance
        """
        try:
            favorite = Favorite.objects.get(pk=pk)
            serializer = FavoriteSerializer(favorite, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area ItineraryItem
        Returns:
            Response -- Empty body with 204 status code
        """
        new_favorite = Favorite.objects.get(pk=pk)
        new_favorite.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            favorite = Favorite.objects.get(pk=pk)
            favorite.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except favorite.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park OrderProducts resource
        Returns:
            Response -- JSON serialized list of park OrderProducts
        """
        Favorites = Favorite.objects.all()
        profileId = self.request.query_params.get('profile_id', None)
        jobId = self.request.query_params.get('job_id', None)
        if jobId is not None:
            Favorites = Favorite.filter(job__id=jobId)

        if profileId is not None:
            Favorites = Favorite.filter(profile__id=profileId)

        serializer = FavoriteSerializer(
            Favorites, many=True, context={'request': request})
        return Response(serializer.data)