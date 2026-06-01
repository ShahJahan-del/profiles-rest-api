from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sms_api import views

router = DefaultRouter()
router.register('departments', views.DepartmentViewSet)
router.register('courses', views.CourseViewSet, basename='courses')
router.register('students', views.StudentViewSet, basename='students')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('enrollments', views.EnrollmentViewSet, basename='enrollments')

urlpatterns = [
    path('', include(router.urls)),
]
