from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    passwd = models.CharField(max_length=100)

    def joindRoomNum(self):
        return len(self.room_set.all())

    def __str__(self):
        return self.name

class Room(models.Model):
    roomName = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def usersNum(self):
        return len(self.users.all())

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

    def ranking(self):
        score_list =  [(self.userTon, self.tonScore, 3),
                       (self.userNan, self.nanScore, 2),
                       (self.userSya, self.syaScore, 1)]
        # sort by score and then by user rank in descending order
        score_list.sort(key = lambda x: (x[1], x[2]), reverse=True)
        return [user.name for user, _, _ in score_list]

class Taikyoku4(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    userTon = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku4_userTon")
    userNan = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku4_userNan")
    userSya = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku4_userSya")
    userPe = models.ForeignKey(User, on_delete=models.CASCADE, related_name="taikyoku4_userPei")
    tonScore = models.IntegerField()
    nanScore = models.IntegerField()
    syaScore = models.IntegerField()
    peScore = models.IntegerField()

    def ranking(self):
        score_list =  [(self.userTon, self.tonScore, 4),
                       (self.userNan, self.nanScore, 3),
                       (self.userSya, self.syaScore, 2),
                       (self.userPe, self.peScore, 1)]
        # sort by score and then by user rank in descending order
        score_list.sort(key = lambda x: (x[1], x[2]), reverse=True)
        return [user.name for user, _, _ in score_list]

class Senseki3(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rankMean = models.FloatField()
    firstNum = models.IntegerField(default=0)
    secondNum = models.IntegerField(default=0)
    thirdNum = models.IntegerField(default=0)
    outNum = models.IntegerField(default=0)
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
    firstNum = models.IntegerField(default=0)
    secondNum = models.IntegerField(default=0)
    thirdNum = models.IntegerField(default=0)
    fourthNum = models.IntegerField(default=0)
    outNum = models.IntegerField(default=0)
    firstRate = models.FloatField()
    secondRate = models.FloatField()
    thirdRate = models.FloatField()
    fourthRate = models.FloatField()
    outRate = models.FloatField()
    gameNum = models.IntegerField()
    scoreMean = models.FloatField()