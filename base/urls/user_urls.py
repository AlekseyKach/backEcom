from django.urls import path
from base.views import user_views as views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/' ,views.RegisterUser , name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/',views.GetUserProfile ,name='user_profile'),
    path('profile/update/',views.UpdateUserProfile ,name='user_profile_update'),
    path('',views.GetUsers ,name='users'),

    

]
