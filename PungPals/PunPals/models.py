from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    rooms = models.ForeignKey(Room,on_delete=models.CASCADE)

class Room(models.Model):

class RoomMid(models.Model):

class UsersInRoom(models.Model):

class Taikyoku3(models.Model):

class Taikyoku3Mid(models.Model):

class Taikyoku4(models.Model):

class Taikyoku4Mid(models.Model):

class Senseki3(models.Model):

class Senseki4(models.Model):
