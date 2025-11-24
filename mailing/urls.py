from django.urls import path
from . import views

app_name = "mailing"

urlpatterns = [
    path("recipients/", views.RecipientListView.as_view(), name="recipient_list"),
    path("recipients/<int:pk>/", views.RecipientDetailView.as_view(), name="recipient_detail", ),
    path("recipients/create/", views.RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/<int:pk>/update/", views.RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", views.RecipientDeleteView.as_view(), name="recipient_delete"),

    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path("mailings/", views.MailingListView.as_view(), name="mailing_list"),
    path("attempts/", views.MailingAttemptListView.as_view(), name="attempt_list"),
]
