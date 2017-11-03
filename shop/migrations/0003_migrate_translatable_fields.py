# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


translatable_models = {
	'Category': ['name', 'slug'],
	'Product': ['name', 'slug', 'description'],
}


def forwards_func(apps, chema_editor):
	for model, fields in translatable_models.items():
		Model = apps.get_model('shop', model)  # apps.get_model(app_label, model_name, require_ready=True)
		ModelTranslation = apps.get_model('shop', '{}Translation'.format(model))
		for obj in Model.objects.all():
			translation_fields = {field: getattr(obj, field) for field in fields}
			translation = ModelTranslation.objects.create(
				master_id=obj.pk,
				language_code=settings.LANGUAGE_CODE,
				**translation_fields)


def backwards_func(apps, schema_editor):
	for model, fields in translatable_models.items():
		Model = apps.get_model('shop', model)
		ModelTranslation = apps.get_model('shop', '{}Translation'.format(model))
		for obj in Model.objects.all():
			translation = _get_translation(obj, ModelTranslation)
			for field in fields:
				setattr(obj, field, getattr(translation, field))
			obj.save()


def _get_translation(obj, MyModelTranslation):
	translations = MyModelTranslation.objects.filter(master_id=obj.pk)
	try:
		return translations.get(language_code=settings.LANGUAGE_CODE)
	except ObjectDoesNotExist:
		return translations.get()

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_add_translation_model'),
    ]

    operations = [
    	migrations.RunPython(forwards_func, backwards_func),
    ]
