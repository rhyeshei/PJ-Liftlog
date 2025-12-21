from rest_framework import serializers
from .models import Workout, SetRecord, ExerciseMaster, MusicAuth, TemplateExercise, Template

# 種目のシリアライザ
class ExerciseMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseMaster
        fields = '__all__'

# セット記録のシリアライザ
class SetRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetRecord
        fields = [
            'id',
            'exercise',
            'set_number',
            'weight',
            'reps',
            'rpe'
        ]

# ワークアウトのシリアライズ
class WorkoutSerializer(serializers.ModelSerializer):
    # セット記録をネストで表示できるようにする
    set_records = SetRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = [
            'id',
            'user',
            'date',
            'start_time',
            'end_time',
            'set_records'
        ]
        read_only_fields = ['user']


class MusicAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicAuth
        # トークン類は機密情報なので、必要最小限のフィールドを定義
        fields = [
            'id', 
            'provider', 
            'access_token', 
            'refresh_token', 
            'expires_at'
        ]
        # 書き込み専用にする(GETでトークンを丸見えにしないための配置)
        extra_kwargs = {
            'access_token': {'write_only': True},
            'refresh_token': {'write_only': True}
        }

class TemplateExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.ReadOnlyField(source='exercise.name')

    class Meta:
        model = TemplateExercise
        fields = [
            'exercise', 
            'exercise_name', 
            'order', 
            'default_sets'
        ]

class TemplateSerializer(serializers.ModelSerializer):
    exercises = TemplateExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Template
        fields = [
            'id', 
            'name', 
            'exercises', 
            'created_at'
        ]