from django.urls import path

from .views import RegisterView, ProfileView, UserLoginView, ActivateEmailView, UserListView, UserToggleActiveView

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("activate/<uidb64>/<token>/", ActivateEmailView.as_view(), name="activate"),

    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/toggle-active/", UserToggleActiveView.as_view(), name="user_toggle_active"),
]
