from django.urls import path
from .views import register, CustomLoginView, logout_view, profile,CustomPasswordChangeView

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path(
    "change-password/",
    CustomPasswordChangeView.as_view(),
    name="change_password"
),
]