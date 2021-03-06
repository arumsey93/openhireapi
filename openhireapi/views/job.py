from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from openhireapi.models import Job, Profile


class JobSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for job
    Arguments:
        serializers
    """
    class Meta:
        model = Job
        url = serializers.HyperlinkedIdentityField(
            view_name='profile',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'user_id', 'title', 'description', 'city', 'state', 'application')
        depth=1


class Jobs(ViewSet):
    """Profiles for Open.HIRE"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Profile instance
        """

        new_job = Job()
        new_job.title = request.data["title"]
        new_job.description = request.data["description"]
        new_job.city = request.data["city"]
        new_job.state = request.data["state"]
        new_job.application = request.data["application"]
        user = request.auth.user
        new_job.user = user

        new_job.save()

        serializer = JobSerializer(new_job, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for job
        Returns:
            Response -- JSON serialized job instance
        """
        try:
            job = Job.objects.get(pk=pk)
            serializer = JobSerializer(job, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a job
        Returns:
            Response -- Empty body with 204 status code
        """

        job = Job.objects.get(pk=pk)
        job.title = request.data["title"]
        job.description = request.data["description"]
        job.city = request.data["city"]
        job.state = request.data["state"]
        job.application = request.data["application"]
        user =  request.auth.user
        job.user = user
        job.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single job
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            job = Job.objects.get(pk=pk)
            job.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Job.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to profile
        Returns:
            Response -- JSON serialized list of jobs
        """
        jobs = Job.objects.all()

        city = self.request.query_params.get('city', None)
        state = self.request.query_params.get('state', None)

        # Support filtering jobs by user id
        job = self.request.query_params.get('user', None)
        if job is not None:
            jobs = jobs.filter(user=request.user)

        if city is not None:
            jobs = jobs.filter(city=city)

        if state is not None:
            jobs = jobs.filter(state=state)

        serializer = JobSerializer(
            jobs, many=True, context={'request': request})
        return Response(serializer.data)