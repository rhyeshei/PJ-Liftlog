
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 'api/'というプレフィックスでliftlog のURLを読み込む
    path('api/', include('liftlog.urls')),
    # ログインしてトークンを取得するためのURL
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    # APIスキーマのダウンロード
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI (ブラウザで確認する用)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')

]
