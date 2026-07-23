from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []  # noqa: RUF012

    operations = [  # noqa: RUF012
        migrations.CreateModel(
            name="PlaceCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField(unique=True)),
                ("name", models.CharField(max_length=100)),
                ("osm_key", models.CharField(max_length=50)),
                ("osm_value", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "place category",
                "verbose_name_plural": "place categories",
                "ordering": ("sort_order", "name"),
            },
        ),
        migrations.AddConstraint(
            model_name="placecategory",
            constraint=models.UniqueConstraint(
                fields=("osm_key", "osm_value"),
                name="unique_place_category_osm_tag",
            ),
        ),
    ]
