from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *


@admin.register(Department, MedicalRecord)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(Profile)
admin.site.register(PatientProfile)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Feedback)
admin.site.register(Wards)
admin.site.register(Billings)
admin.site.register(Prescription)