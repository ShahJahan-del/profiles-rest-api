from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from sms_api import models, serializers, permissions
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models import Max

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

    # INTERCEPTION DE LA CRÉATION POUR L'ENVOI D'EMAIL
    def perform_create(self, serializer):
        # 1. On sauvegarde l'inscription en base de données (Supabase)
        enrollment = serializer.save()

        # 2. On récupère dynamiquement les objets liés pour personnaliser le message
        student = enrollment.student
        course = enrollment.course

        # 3. Rédaction de l'e-mail
        subject = f"Confirmation d'inscription : {course.title}"
        message = (
            f"Bonjour {student.first_name} {student.last_name},\n\n"
            f"Nous te confirmons ton inscription au cours '{course.title}' "
            f"dispensé par le professeur {course.teacher.first_name} {course.teacher.last_name}.\n\n"
            f"Cordialement,\nL'administration de l'école."
        )
        recipient_list = [student.email]

        # 4. Envoi via le système natif de Django
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@ecole.fr',
            recipient_list=recipient_list,
            fail_silently=False, # Permet de lever une erreur dans le terminal si l'envoi échoue
        )

class AdminUserManagementViewSet(viewsets.ModelViewSet):
    """Gestion des comptes par l'Admin + Envoi d'email (Section 10.2)"""
    serializer_class = serializers.AdminUserCreationSerializer
    queryset = User.objects.all()

    # Seul l'utilisateur ayant le rôle 'ADMIN' a le droit d'accéder à ce ViewSet
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # 1. Récupération des données saisies
        raw_password = self.request.data.get('password')
        role = self.request.data.get('role')

        # 2. Sauvegarde de l'utilisateur dans la table d'authentification (Monde 1)
        user = serializer.save()

        # 3. LIAISON SÉCURISÉE AVEC SUPABASE (Monde 2)
        if role == 'TEACHER':
            #utilisation de Max direct
            max_id = models.Teachers.objects.aggregate(Max('teacher_id'))['teacher_id__max']
            next_id = (max_id or 0) + 1

            models.Teachers.objects.create(
                teacher_id=next_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )

        elif role == 'STUDENT':
            #utilisation de Max direct
            max_id = models.Students.objects.aggregate(Max('student_id'))['student_id__max']
            next_id = (max_id or 0) + 1

            models.Students.objects.create(
                student_id=next_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                age_category="Adult",
                sex="Not Specified"
            )

        # 4. Envoi de l'e-mail
        subject = f"Vos identifiants de connexion - École ({role})"
        message = (
            f"Bonjour {user.first_name} {user.last_name},\n\n"
            f"L'administrateur vous a créé un compte avec le rôle : {role}.\n\n"
            f"Voici vos accès pour vous connecter :\n"
            f" - Identifiant (Username) : {user.username}\n"
            f" - Mot de passe : {raw_password}\n\n"
            f"Cordialement,\nL'administration."
        )
        send_mail(subject, message, 'noreply@ecole.fr', [user.email], fail_silently=False)
