from rest_framework import serializers
from moviesapp.models import Rating,Movie


class MovieSerializer(serializers.ModelSerializer):
    '''
    Movie model serialzier 
    - has custom field named 'rating' to return average movie ratings based on function declared inside \n
    models file . 
    '''
    id = serializers.IntegerField(read_only=True)
    rating =  serializers.FloatField(source='get_ratings_avg',read_only=True)
    class Meta : 
        model = Movie
        fields = ('id','title','rating')



class RatingSerializer(serializers.ModelSerializer):
    '''
    Rating model serialzier  
    '''
    id = serializers.IntegerField(read_only=True)
    movie = serializers.IntegerField(source='movie_id',read_only=True)
    class Meta : 
        model = Rating
        fields = ('id','value','movie')

    def validate(self, data):
        '''
        overriding serializer validation to validate that rating value is \n
        within allowed range [1,5] .
        '''
        value = self.context['value']
        if value not in range(1,6) :
            raise serializers.ValidationError({'value':'value is invalid , must be an integer within range [1,5]'}) 
        return data 
    
    # {"value" :"a","movie_id":9}