from django.conf import settings
from django.urls import include, path

from school.views import students_list

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('', students_list, name='students'),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
else:
    urlpatterns = [
        path('', students_list, name='students'),
    ]
