from __future__ import annotations

from typing import Any, ClassVar, Self

from django.db import models
from django.utils.text import slugify

from apps.content.storages import OverwriteStorage


def project_thumbnail_path(instance: Project, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    return f"projects/{instance.slug}.{ext}"


class Project(models.Model):
    slug = models.SlugField(max_length=140, unique=True)
    thumbnail = models.ImageField(
        upload_to=project_thumbnail_path,
        storage=OverwriteStorage(),
    )
    title_pt = models.CharField(max_length=120)
    title_en = models.CharField(max_length=120)
    short_description_pt = models.TextField()
    short_description_en = models.TextField()
    project_url = models.URLField()
    read_more_url = models.URLField(blank=True, null=True)
    code_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["order", "-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        return self.title_pt

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            base = slugify(self.title_en or self.title_pt) or "project"
            slug = base
            i = 1
            qs = Project.objects.exclude(pk=self.pk) if self.pk else Project.objects.all()
            while qs.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        return (0, {})

    @classmethod
    def load(cls) -> Self:
        obj, _ = cls._default_manager.get_or_create(pk=1)
        return obj


class AboutMe(SingletonModel):
    content_pt = models.TextField(blank=True)
    content_en = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Me"
        verbose_name_plural = "About Me"

    def __str__(self) -> str:
        return "About Me"


class Resume(SingletonModel):
    file_pt = models.FileField(upload_to="resume/", blank=True)
    file_en = models.FileField(upload_to="resume/", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resume"

    def __str__(self) -> str:
        return "Resume"
