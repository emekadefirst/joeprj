from . import views
from django.urls import path



urlpatterns = [
    path('programs', views.ProgramView.as_view(), name="programs-list-create"),
    path('programs/<int:pk>', views.ProgramRetrieveUpdateDestroyView.as_view(), name="programs-retrieve-update-delete"),

    # Daily Study
    path('daily-study', views.DailyStudyView.as_view(), name="daily-study-list-create"),
    path('daily-study/<int:pk>', views.DailyStudyRetrieveUpdateDestroyView.as_view(), name="daily-study-retrieve-update-delete"),

    # notifications
    path('api/register-device/', views.register_device),
    path('test-notification/', views.test_notification, name="Test notifcation")
]