from django.db import models
from django.db.models import Sum

# Movie Model
class Movie(models.Model) : 
    '''
    - The movie model contains 1 field : title 
    - There is a foreign key declared in Rating model to access all \n
      related movie rating . It can accessed using this convention : \n 
      {movieObj}.movie_ratings.all()
    '''
    title = models.CharField(max_length=200,default='')


    def __str__(self) : 
        return self.title
    
    def get_ratings_avg(self):
        all_ratings =   self.movie_ratings.all()
        sum_ratings = all_ratings.aggregate(total=Sum('value'))['total']
        avg = round(sum_ratings / all_ratings.count(),2) if all_ratings.exists() else 0
        return avg



class Rating(models.Model) : 
    movie = models.ForeignKey('Movie',related_name='movie_ratings',on_delete=models.CASCADE)
    value = models.IntegerField(default=0)


    def __str__(self) : 
        return '%s has a rating of %s'%(self.movie.title,self.value)