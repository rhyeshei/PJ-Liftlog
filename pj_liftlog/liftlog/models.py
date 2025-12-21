from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings



# 1.ユーザーモデル
class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    lift_history = models.TextField(blank=True)

    def __str__(self):
        return self.username

# 2.　音楽連携モデル
class MusicAuth(models.Model):
    # Userと1対1の関係
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='music_auth')
    
    # サービス名(Apple/Spotify)
    PROVIDER_CHOICES = [
        ('spotify', 'Spotify'),
        ('apple', 'Apple Music'),
    ]
    provider = models.CharField(
        max_length=20,
        choices = PROVIDER_CHOICES
    )

    # 安全なストレージに保管すべきトークン類
    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.provider}" 

# 3. 種目マスタ
class ExerciseMaster(models.Model):
    # 種目名は、直接DBへ入力
    name = models.CharField(max_length=255, unique=True)

    # 部位の選択＋otherで自由記入
    BODY_PART_CHOICES = [
        ('chest', '胸'),
        ('back', '背中'),
        ('shoulders','肩'),
        ('triceps', '上腕三頭筋'),
        ('biceps', '上腕二頭筋'),
        ('abs', '腹筋'),
        ('legs', '脚'),
        ('glutes', '尻'),
        ('other', 'その他')
    ]

    body_part = models.CharField(
        max_length=50,
        choices=BODY_PART_CHOICES
    )

    body_part_other = models.CharField(
        max_length=100,
        blank=True
    )
    # 動作タイプの選択
    MOVEMENT_CHOICES =[
        ('push', 'Push'),
        ('pull', 'Pull'),
        ('squat', 'Squat'),
        ('hinge', 'Hinge'),
        ('core', 'Core'),
        ('other', 'その他')
    ]
    
    movement = models.CharField(
        max_length=50,
        choices=MOVEMENT_CHOICES
    )
    # name で呼ばせる
    def __str__(self):
        return self.name
    
    rest_time_seconds = models.PositiveIntegerField(default=60)
    
# 4. ワークアウト（親）
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

# 5. セット記録（子）
class SetRecord(models.Model):
    workout = models.ForeignKey(
        Workout,
        related_name='set_records',
        on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(ExerciseMaster,on_delete=models.PROTECT)
    set_number = models.PositiveIntegerField()
    weight = models.FloatField()
    reps = models.PositiveIntegerField()
    rpe = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(10)],
        null=True,
        blank=True
    )

# 6.　テンプレート
class Template(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class TemplateExercise(models.Model):
    template = models.ForeignKey(Template, related_name='exercises', on_delete=models.CASCADE)
    exercise = models.ForeignKey(ExerciseMaster, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    default_sets = models.PositiveIntegerField(default=3)
