from django.utils import timezone
from django.db.models import Sum, Max, F
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Workout, ExerciseMaster, SetRecord, MusicAuth, Template, TemplateExercise
from .serializers import WorkoutSerializer, ExerciseMasterSerializer, SetRecordSerializer, MusicAuthSerializer, TemplateSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all
    serializer_class = WorkoutSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    # POST /api/workouts/start/ : ワークアウト開始
    @action(detail=False, methods=['post'])
    def start(self, request):
        workout = Workout.objects.create(
            user = request.user,
            date = timezone.now().date(),
            start_time = timezone.now()
        )
        serializer = self.get_serializer(workout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # POST /api/workouts/{id}/sets/ : セットの保存
    @action(detail=True, methods=['post'])
    def sets(self, request, pk=None):
        workout = self.get_object()
        serializer = SetRecordSerializer(data=request.data)
        
        if serializer.is_valid():
            set_record = serializer.save(workout=workout)
            
            # セット完了後、次のタイマー時間を取得
            rest_time = set_record.exercise.rest_time_seconds

            return Response({
                "message": "セットを記録しました",
                "data": serializer.data,
                "rest_time_seconds": rest_time
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # ：ワークアウトの終了
    @action(detail=True, methods=['post'])
    def finish(self,request, pk=None):
        workout = self.get_object()
        workout.end_time = timezone.now
        workout.save()
        return Response(
            self.get_serializer(workout).data,
            status=status.HTTP_200_OK
        )
    

class ExerciseMasterViewSet(viewsets.ModelViewSet):
    queryset = ExerciseMaster.objects.all()
    serializer_class = ExerciseMasterSerializer

class MusicAuthView(APIView):
    permission_classes = [IsAuthenticated]

    # GET/api/music/auth/：認証URLの取得
    def get(self, request):
        # 本来はここでSpotify/Appleの認証画面URLを生成して返します [cite: 74]
        data = {
            "spotify_auth_url": "https://accounts.spotify.com/authorize?...",
            "apple_music_auth_url": "https://music.apple.com/..."
        }
        return Response(data)
    
    # POST/api/music/callback/：トークンの保存
    def post(self, request):
        serializer = MusicAuthSerializer(data=request.data)
        if serializer.is_valid():
            # すでに連携済みなら更新、なければ新規作成
            MusicAuth.objects.update_or_create(
                user = request.user,
                defaults=serializer.validated_data
            )
            return Response({"message":"連携が完了しました"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PlayListView(APIView):
    permission_classes = [IsAuthenticated]

    # GET/api/music/playlist/：プレイリスト一覧取得
    def get(self, request):
        # ここでは本来、保存されたトークンを使って外部SDK/APIを叩きます
        # 今回は流れを確認するためのダミーデータを返します
        dummy_playlists = [
            {"id": "pl1", "name": "脚トレ用爆音リスト", "provider": "Spotify"},
            {"id": "pl2", "name": "集中用Lo-fi", "provider": "Apple Music"}
        ]
        return Response(dummy_playlists)
    

class WorkoutAnalyticsViews(APIView):
    permission_classes = [IsAuthenticated]

    # 重量推移や部位別ボリュームを集計するAPI
    def get(self, request):
        user = request.user

        # 1. 部位別vol.の集計
        # 重量　×　レップ数 を計算し、部位ごとに合計
        volume_qs = (
            SetRecord.objects.filter(workout__user=user)
            .values(part=F('exercise__body_part'))
            .annotate(total_volume=Sum('weight') * F('reps'))
            .order_by('-total_volume')
        )

        weight_qs = (
            SetRecord.objects.filter(workout__user=user)
            .values(date=F('workout__date'), name=F('exercise__name'))
            .annotate(max_weight=Max('weight'))
            .order_by('date')
        )


        #2.　重量の推移
        # ① 部位別ボリューム（グラフ用整形）
        volume_labels = []
        volume_data = []

        for row in volume_qs:
            volume_labels.append(row["part"])
            volume_data.append(row["total_volume"])
        
        volume_response = {
            "labels": volume_labels,
            "datasets": [
                {
                    "labels": "部位別ボリューム",
                    "data": volume_data
                }
            ]
        }

        # ② 重量推移（折れ線用整形）
        from collections import defaultdict
        labels = []
        series = defaultdict(list)

        for row in weight_qs:
            date = row["date"]
            name = row["name"]

            if date not in labels:
                labels.append(date)
            
            series[name].append(row["max_weight"])
        
        weight_response = {
            "labels": labels,
            "datasets": [
                {"labels": name, "data": data}
                for name, data in series.items()
            ]
        }

        return Response({
            "volume_by_part": volume_response,
            "weight_progress": weight_response
        })
    

class TemplateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TemplateSerializer

    def get_queryset(self):
        return Template.objects.filter(user = self.request.user)

    # POST/api/templates/create_from_workout/：過去の記録からのテンプレ
    @action(detail=False, methods=['post'])
    def create_from_workout(self, request):
        workout_id = request.data.get('workout_id')
        template_name = request.data.get('name', '新しいテンプレート')

        workout = get_object_or_404(
            Workout,
            id = workout_id,
            user = request.user
        )

        # テンプレート本体を作成
        template = Template.objects.create(user=request.user, name=template_name)

        # ワークアウト内のユニークな種目を抽出してテンプレートに記録
        exercises = workout.set_record.values('exercise').distinct()
        for i, item in enumerate(exercises):
            TemplateExercise.objects.create(
                template = template,
                exercise_id = item['exercise'],
                order = i,
                default_sets = 3
            )
        return Response(TemplateSerializer(template).data, status=status.HTTP_201_CREATED)
    
    # POST/api/templates/{id}/apply/：テンプレートを適用してワークアウト開始
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        template = self.get_object()

        # 新しいワークアウトを作成
        new_workout = Workout.objects.create(
            user = request.user,
            date = timezone.now().date(),
            start_time = timezone.now()
        )

        # テンプレートの種目に基づいて空のセット（または前回の重量）を準備するロジックをここに書く
        # ※フロントエンド側でこの種目リストを元に入力画面を構成する形でもOK
        
        return Response({
            "workout_id": new_workout.id, 
            "message": "テンプレートを適用しました"
        })