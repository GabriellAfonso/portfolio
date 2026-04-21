from typing import TypedDict

from apps.content.repositories.project_repository import ProjectRepository


class ProjectDTO(TypedDict):
    id: int
    thumbnail_url: str
    title: str
    short_description: str
    project_url: str
    read_more_url: str | None
    code_url: str | None


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    def list_active(self, language: str) -> list[ProjectDTO]:
        suffix = "en" if _is_english(language) else "pt"
        return [
            ProjectDTO(
                id=p.pk,
                thumbnail_url=p.thumbnail.url if p.thumbnail else "",
                title=getattr(p, f"title_{suffix}"),
                short_description=getattr(p, f"short_description_{suffix}"),
                project_url=p.project_url,
                read_more_url=p.read_more_url,
                code_url=p.code_url,
            )
            for p in self.repository.list_active()
        ]


def _is_english(language: str) -> bool:
    return language.lower().startswith("en")
