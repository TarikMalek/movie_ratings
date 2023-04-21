from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from django.http import Http404


from serializers.MovieSerializer import MovieSerializer,RatingSerializer
from moviesapp.models import Movie




class MoviesList(APIView):
    """
    List all movies, or create a new movie.
    """
    permission_classes = (permissions.AllowAny,)
  
    def get(self, request, format=None):
        ''' 
        list all movies in the database 
        curl --header "Content-Type: application/json" -X GET http://127.0.0.1:8000/movies/

        '''
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''
        create a new movie 
        curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/movies/ --data '{"title":"test movie7"}'
        '''
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    """
    Retrieve, update or delete a movie instance.
    """
    permission_classes = (permissions.AllowAny,)

    def get_object(self, id):
        try:
            return Movie.objects.get(pk=id)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        '''
        get single movie with id 
        curl --header "Content-Type: application/json" -X GET http://127.0.0.1:8000/movies/{id}/
        '''
        Movie = self.get_object(id)
        serializer = MovieSerializer(Movie)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        '''
        update single movie with id 
        curl --header "Content-Type: application/json" -X PUT http://127.0.0.1:8000/movies/7/ --data '{"title":"test movie77"}'
        '''
        Movie = self.get_object(id)
        serializer = MovieSerializer(Movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        '''
        delete single movie with id 
        curl --header "Content-Type: application/json" -X DELETE http://127.0.0.1:8000/movies/{id}/
        '''
        Movie = self.get_object(id)
        Movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class RatingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        '''
        create a new movie rating 
        curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/ratings/ --data '{"value":5,"movie_id":1}'
        '''
        data = request.data
        movie_id = data['movie_id']
        movie = None
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise Http404
        
        value = data['value']
        serializer = RatingSerializer(data=request.data,context={'value':value})
        if serializer.is_valid():
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



