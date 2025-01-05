from .models import Department, MedicalRecord
from modeltranslation.translator import TranslationOptions,register

@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('department_name', )


@register(MedicalRecord)
class MedicalRecordTranslationOptions(TranslationOptions):
    fields = ('diagnosis', 'treatment')
