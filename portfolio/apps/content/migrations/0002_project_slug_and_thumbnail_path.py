from __future__ import annotations

from typing import Any

from django.db import migrations, models
from django.utils.text import slugify

import apps.content.models
import apps.content.storages


def populate_slugs(apps: Any, schema_editor: Any) -> None:
    Project = apps.get_model("content", "Project")
    used: set[str] = set()
    for project in Project.objects.all():
        base = slugify(project.title_en or project.title_pt) or f"project-{project.pk}"
        slug = base
        i = 1
        while slug in used:
            slug = f"{base}-{i}"
            i += 1
        used.add(slug)
        project.slug = slug
        project.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [("content", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="project",
            name="slug",
            field=models.SlugField(max_length=140, null=True, unique=True),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="project",
            name="slug",
            field=models.SlugField(max_length=140, unique=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="thumbnail",
            field=models.ImageField(
                storage=apps.content.storages.OverwriteStorage(),
                upload_to=apps.content.models.project_thumbnail_path,
            ),
        ),
    ]
