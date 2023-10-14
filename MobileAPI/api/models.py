from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'pereval_user'


class Pereval(models.Model):
    STATUSES = [
        ('NW', 'Новое'),
        ('PD', 'В процессе'),
        ('AC', 'Информация принята'),
        ('RJ', 'Информация не принята')
    ]

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    connect = models.CharField(max_length=255, blank=True)
    add_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coordinates = models.ForeignKey('Coords', on_delete=models.CASCADE)
    levels = models.ForeignKey('Level', blank=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=2, choices=STATUSES, default='NW')

    class Meta:
        db_table = 'pereval_add'


class Level(models.Model):
    winter_level = models.CharField(max_length=2, blank=True)
    summer_level = models.CharField(max_length=2, blank=True)
    autumn_level = models.CharField(max_length=2, blank=True)
    spring_level = models.CharField(max_length=2, blank=True)

    class Meta:
        db_table = 'pereval_level'


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    class Meta:
        db_table = 'pereval_coords'


class Images(models.Model):
    pereval = models.ForeignKey(Pereval, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    data = models.BinaryField()

    class Meta:
        db_table = 'pereval_images'
