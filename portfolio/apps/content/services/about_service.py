from apps.content.repositories.about_repository import AboutRepository


class AboutService:
    def __init__(self, repository: AboutRepository) -> None:
        self.repository = repository

    def get(self, language: str) -> str:
        about = self.repository.get()
        if language.lower().startswith("en"):
            return about.content_en
        return about.content_pt
