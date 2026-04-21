from django.db.models import QuerySet

from apps.content.models import Project


class ProjectRepository:
    def list_active(self) -> QuerySet[Project]:
        return Project.objects.filter(is_active=True)
