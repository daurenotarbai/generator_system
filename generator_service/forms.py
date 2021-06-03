from django import forms

from generator_service.models import TblSchemaColumns, TblSchemaBasicInfo


class SchemaColumnsForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(SchemaColumnsForm, self).__init__(*args, **kargs)

    class Meta:
        model = TblSchemaColumns
        fields = '__all__'


class SchemaBasicInfoForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(SchemaBasicInfoForm, self).__init__(*args, **kargs)

    class Meta:
        model = TblSchemaBasicInfo
        fields = '__all__'
