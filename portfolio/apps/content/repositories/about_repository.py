from apps.content.models import AboutMe


class AboutRepository:
    def get(self) -> AboutMe:
        return AboutMe.load()
