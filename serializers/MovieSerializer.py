from rest_framework import serializers
from moviesapp.models import Rating,Movie


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    rating =  serializers.FloatField(source='get_ratings_avg',read_only=True)
    class Meta : 
        model = Movie
        fields = ('id','title','rating')



class RatingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    movie = serializers.IntegerField(source='movie_id',read_only=True)
    class Meta : 
        model = Rating
        fields = ('id','value','movie')

    def validate(self, data):
        value = self.context['value']
        if value not in range(1,6):
            raise serializers.ValidationError({'value':'vaue is invalid , must be within range [1,5]'}) 
        return data 