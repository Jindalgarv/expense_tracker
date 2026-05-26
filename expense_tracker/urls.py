from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
]
