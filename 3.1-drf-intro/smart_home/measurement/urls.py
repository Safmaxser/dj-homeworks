from django.urls import path

from .views import SensorsListView, SensorView, MeasurementsView

urlpatterns = [
    path('sensors/', SensorsListView.as_view()),
    path('sensors/<int:pk>/', SensorView.as_view()),
    path('measurements/', MeasurementsView.as_view()),
]
