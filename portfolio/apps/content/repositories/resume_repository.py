from apps.content.models import Resume


class ResumeRepository:
    def get(self) -> Resume:
        return Resume.load()
