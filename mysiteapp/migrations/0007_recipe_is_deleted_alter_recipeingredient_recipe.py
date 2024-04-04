# Generated by Django 5.0.3 on 2024-04-04 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysiteapp', '0006_category_ingredient_recipe_image_recipeingredient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='mysiteapp.recipe'),
        ),
    ]