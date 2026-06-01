from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Permet l'accès complet uniquement aux Admins"""
    def has_permission(self, request, view):
        # On vérifie si l'utilisateur est connecté et si son rôle est ADMIN
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN'

class IsTeacherUser(permissions.BasePermission):
    """Permet l'accès aux professeurs connectés"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'TEACHER'

class IsStudentUser(permissions.BasePermission):
    """Permet l'accès aux étudiants connectés"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'STUDENT'
