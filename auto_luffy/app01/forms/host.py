#_*_coding:utf-8_*_
from django import forms
from django.core.exceptions import ValidationError
from app01 import models

class  HostModelForm(forms.ModelForm):
    class Meta:
        model = models.Host
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HostModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'