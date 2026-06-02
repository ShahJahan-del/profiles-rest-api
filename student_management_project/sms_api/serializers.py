from rest_framework import serializers
from sms_api import models
from django.contrib.auth.models import User

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Departments
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Courses
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Students
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teachers
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enrollments
        fields = '__all__'

class AdminUserCreationSerializer(serializers.ModelSerializer):
    """Création de compte par l'Admin (Inspiré Section 10.1)"""
    role = serializers.ChoiceField(choices=(('ADMIN', 'Admin'), ('TEACHER', 'Teacher'), ('STUDENT', 'Student')), write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'role')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        # 1. On extrait le rôle envoyé par le formulaire ('ADMIN', 'TEACHER', 'STUDENT')
        role = validated_data.pop('role')

        # 2. On crée l'utilisateur Django standard
        user = User.objects.create_user(**validated_data)

        # 3. ON FIXE LES DROITS DJANGO EN FONCTION DU RÔLE
        if role == 'ADMIN':
            user.is_staff = True      # Donnes l'accès au panel /admin/
            user.is_superuser = True  # Donne tous les super-pouvoirs
        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()
        return user
