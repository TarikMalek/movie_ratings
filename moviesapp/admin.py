from django.contrib import admin
from moviesapp.models import Movie,Rating

# Register your models here.



class MovieModelAdmin(admin.ModelAdmin):
    model = Movie
    list_display = ('id','title','rating')

    readonly_fields=('rating',)
    def rating(self, obj):
        return obj.get_ratings_avg()
    rating.short_description = 'Rating'
   
admin.site.register(Movie,MovieModelAdmin)
admin.site.register(Rating)