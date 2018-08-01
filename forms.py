"""Species application forms"""
from django import forms
from django.utils.translation import gettext as _

from collections import Counter
from tinymce.widgets import TinyMCE

from .models import Species, AdditionalInfo


class SpeciesForm(forms.ModelForm):
    """Form for basic species informations"""

    class Meta:
        model = Species
        fields = '__all__'

    def clean_additional_infos(self):
        """Check and prevent adding multiple same info_keys of additional
        informations
        """
        addi_info_objects = self.cleaned_data['additional_infos']
        info_keys = [addi_object.info_key for addi_object in addi_info_objects]
        info_keys_count = Counter(info_keys)
        for info_key, occurrences in info_keys_count.items():
            if occurrences > 1:
                raise forms.ValidationError(
                    _('Invalid value: multiple %(info_key)s'),
                    params={'info_key': info_key},
                    code='invalid'
                    )
        return addi_info_objects


class AdditionalInfoForm(forms.ModelForm):
    """Form for additional species informations"""
    info_value = forms.CharField(widget=TinyMCE(attrs={'rows': 20}))

    class Meta:
        model = AdditionalInfo
        fields = '__all__'
