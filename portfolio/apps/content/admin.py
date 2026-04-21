from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString

from apps.content.models import AboutMe, Project, Resume


if TYPE_CHECKING:
    _ProjectAdminBase = admin.ModelAdmin[Project]
    _AboutAdminBase = admin.ModelAdmin[AboutMe]
    _ResumeAdminBase = admin.ModelAdmin[Resume]
else:
    _ProjectAdminBase = admin.ModelAdmin
    _AboutAdminBase = admin.ModelAdmin
    _ResumeAdminBase = admin.ModelAdmin


@admin.register(Project)
class ProjectAdmin(_ProjectAdminBase):
    list_display = ("title_pt", "order", "is_active", "thumbnail_preview")
    list_editable = ("order", "is_active")
    search_fields = ("title_pt", "title_en")
    ordering = ("order",)
    readonly_fields = ("thumbnail_preview",)
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "thumbnail",
                    "thumbnail_preview",
                    "project_url",
                    "read_more_url",
                    "code_url",
                )
            },
        ),
        ("Portuguese", {"fields": ("title_pt", "short_description_pt")}),
        ("English", {"fields": ("title_en", "short_description_en")}),
        ("Display", {"fields": ("order", "is_active")}),
    ]

    @admin.display(description="Preview")
    def thumbnail_preview(self, obj: Project) -> SafeString:
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.thumbnail.url)
        return SafeString("")


@admin.register(AboutMe)
class AboutMeAdmin(_AboutAdminBase):
    fieldsets = [
        ("Portuguese", {"fields": ("content_pt",)}),
        ("English", {"fields": ("content_en",)}),
    ]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not AboutMe.objects.exists()

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: AboutMe | None = None,
    ) -> bool:
        return False


@admin.register(Resume)
class ResumeAdmin(_ResumeAdminBase):
    fieldsets = [
        ("Portuguese", {"fields": ("file_pt",)}),
        ("English", {"fields": ("file_en",)}),
    ]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not Resume.objects.exists()

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Resume | None = None,
    ) -> bool:
        return False
