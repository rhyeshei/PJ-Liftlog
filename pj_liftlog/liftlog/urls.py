from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutViewSet, MusicAuthView, PlayListView, WorkoutAnalyticsViews, TemplateViewSet

# Routerを使ってViewSetを自動的にURLに紐付ける
router = DefaultRouter()
router.register(r'workout', WorkoutViewSet, basename='workout')
router.register(r'templates', TemplateViewSet, basename='template')

urlpatterns = [
    # /api/の後に続くルートを登録
    path('', include(router.urls)),
    path('music/auth/', MusicAuthView.as_view(), name='music-auth'),
    path('music/playlist/', PlayListView.as_view(), name='music-playlist'),
    path('analytics', WorkoutAnalyticsViews.as_view(), name='workout-analytics'),
]