from django.db import models
from django.utils.text import slugify
#Dataset design to save data
class List(models.Model):
    slug = models.SlugField(unique=True, blank=False) #Unique name for name for easy access
    title = models.CharField(max_length=120)
    key = models.CharField(max_length=120,blank= True)

    def filtered_non_complete(self): #Filter and return only tasks that are not complete according to the unique name
        master = List.objects.get(slug=self.slug)
        return Task.objects.filter(complete=False, list = master)

    def filtered_complete(self):  #Filter and return only tasks that are complete according to the unique name
        master = List.objects.get(slug=self.slug)
        return Task.objects.filter(complete=True, list = master)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while List.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
            self.key = self._get_unique_slug()

        super().save(*args, **kwargs)

class Task(models.Model):
    list = models.ForeignKey(List, blank=False, #Link tasks to a list object using FK
                    on_delete=models.CASCADE,
                    default=1, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True) #Time of creation
    updated_at = models.DateTimeField(auto_now=True) #Show a time step for the last update
    slug = models.SlugField(unique=True, blank=False) # Ensure unique for easy access
    complete = models.BooleanField(default=False) # State if a task is complete, Default = False
    name= models.CharField(max_length=120)


    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Task.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
