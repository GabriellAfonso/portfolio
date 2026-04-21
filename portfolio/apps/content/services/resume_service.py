from django.db.models.fields.files import FieldFile

from apps.content.repositories.resume_repository import ResumeRepository


class ResumeService:
    def __init__(self, repository: ResumeRepository) -> None:
        self.repository = repository

    def get_file(self, language: str) -> FieldFile | None:
        resume = self.repository.get()
        file = resume.file_en if language.lower().startswith("en") else resume.file_pt
        if not file:
            return None
        return file
