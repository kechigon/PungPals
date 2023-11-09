from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, password, **extra_fields):
        if not username or not password:
            raise ValueError("Name and password field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(username, password, **extra_fields), 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    def __str__(self):
        return self.username      

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    passwd = models.CharField(max_length=100)
    users = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name

class Taikyoku3(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    userTon = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="taikyoku3_userTon")
    userNan = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="taikyoku3_userNan")
    userSya = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tiakyoku3_userSya")
    tonScore = models.IntegerField()
    nanScore = models.IntegerField()
    syaScore = models.IntegerField()

    def ranking(self):
        score_list =  [(self.userTon, self.tonScore, 3),
                       (self.userNan, self.nanScore, 2),
                       (self.userSya, self.syaScore, 1)]
        # sort by score and then by user rank in descending order
        score_list.sort(key = lambda x: (x[1], x[2]), reverse=True)
        return [(user.name, score) for user, score, _ in score_list]

class Taikyoku4(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    userTon = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="taikyoku4_userTon")
    userNan = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="taikyoku4_userNan")
    userSya = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="taikyoku4_userSya")
    userPe = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="taikyoku4_userPei")
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
        return [(user.name, score) for user, score, _ in score_list]

class Senseki3(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rankMean = models.FloatField(default=0)
    firstNum = models.IntegerField(default=0)
    secondNum = models.IntegerField(default=0)
    thirdNum = models.IntegerField(default=0)
    outNum = models.IntegerField(default=0)
    firstRate = models.FloatField()
    secondRate = models.FloatField()
    thirdRate = models.FloatField()
    outRate = models.FloatField()
    gameNum = models.IntegerField()
    scoreSum = models.BigIntegerField()
    scoreMean = models.FloatField()

class Senseki4(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    scoreSum = models.BigIntegerField()
    scoreMean = models.FloatField()