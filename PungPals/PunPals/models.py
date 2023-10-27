from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    passwd = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    roomName = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.roomName

class Taikyoku3(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    userTon = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku3_userTon")
    userNan = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku3_userNan")
    userSya = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tiakyoku3_userSya")
    tonScore = models.IntegerField()
    nanScore = models.IntegerField()
    syaScore = models.IntegerField()

class Taikyoku4(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    userTon = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku4_userTon")
    userNan = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku4_userNan")
    userSya = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku4_userSya")
    userPe = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku4_userPei")
    tonScore = models.IntegerField()
    NanScore = models.IntegerField()
    SyaScore = models.IntegerField()
    PeScore = models.IntegerField() 

class Senseki3(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rankMean = models.FloatField()
    firstNum = models.IntegerField()
    secondNum = models.IntegerField()
    thirdNum = models.IntegerField()
    firstRate = models.FloatField()
    secondRate = models.FloatField()
    thirdRate = models.FloatField()
    outRate = models.FloatField()
    gameNum = models.IntegerField()
    scoreMean = models.FloatField()

class Senseki4(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rankMean = models.FloatField()
    firstNum = models.IntegerField()
    secondNum = models.IntegerField()
    thirdNum = models.IntegerField()
    fourthNum = models.IntegerField()
    firstRate = models.FloatField()
    secondRate = models.FloatField()
    thirdRate = models.FloatField()
    fourthRate = models.FloatField()
    outRate = models.FloatField()
    gameNum = models.IntegerField()
    scoreMean = models.FloatField()