from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from sms_api import models, serializers, permissions

# Create your views here.

class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Departments.objects.all()
    # Seul l'admin peut toucher aux départements
    permission_classes = [permissions.IsAdminUser]

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer

    def get_permissions(self):
        # L'admin peut tout faire (CRUD), le prof peut juste voir (Read-Only)
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()] # Il faut juste être connecté
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        # Si c'est un prof, il ne voit QUE ses cours assignés
        if getattr(user, 'role', None) == 'TEACHER':
            return models.Courses.objects.filter(teacher_id=user.id)
        # L'admin voit tout
        return models.Courses.objects.all()

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentSerializer

    def get_permissions(self):
        # L'admin peut gérer les profils, les profs et étudiants peuvent juste voir
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        # Un étudiant ne peut voir QUE son propre profil
        if getattr(user, 'role', None) == 'STUDENT':
            return models.Students.objects.filter(student_id=user.id)
        # Un prof ne peut voir que les étudiants inscrits dans SES cours
        if getattr(user, 'role', None) == 'TEACHER':
            return models.Students.objects.filter(enrollments__course__teacher_id=user.id).distinct()
        # L'admin voit tout
        return models.Students.objects.all()

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeacherSerializer

    # Seul l'admin peut modifier la liste globale des profs,
    # mais les utilisateurs connectés peuvent la consulter
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        # Tout le monde voit la liste des profs
        return models.Teachers.objects.all()

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EnrollmentSerializer

    def get_permissions(self):
        # L'admin et le Teacher peuvent gérer les inscriptions
        if getattr(self.request.user, 'role', None) == 'TEACHER' or getattr(self.request.user, 'role', None) == 'ADMIN':
            return [IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        # Le prof ne voit que les inscriptions aux cours qu'il donne
        if getattr(user, 'role', None) == 'TEACHER':
            return models.Enrollments.objects.filter(course__teacher_id=user.id)
        # L'étudiant ne voit que ses propres inscriptions
        if getattr(user, 'role', None) == 'STUDENT':
            return models.Enrollments.objects.filter(student_id=user.id)
        return models.Enrollments.objects.all()
