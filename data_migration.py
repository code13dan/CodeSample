# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_m2m_species_additionalinfo(apps, schema_editor):
    """Populate database tables Species, AdditionalInfo many to many relation
    with data from okzi.doNotClick
    """

    Species = apps.get_model('species', 'Species')
    AdditionalInfo = apps.get_model('species', 'AdditionalInfo')

    # paset from species_system_raw_text-final_table_format.csv
    # species_addi_infos = {genus_latin_name: [addi_info_id,...],...}
    species_addi_infos = {
        'Acanthognathus ocellatus': ['1','2','3','4','5','20',],
        'Acanthognathus teledectus': ['1','2','3','4','5','20',],
    }

    # get all additional informations from database
    all_addi_infos = {str(addi_obj.id): addi_obj for
                      addi_obj in AdditionalInfo.objects.all()}

    # push it to database
    for species, addi_id_list in species_addi_infos.items():
        species = Species.objects.get(latin_name=species)
        addi_infos_list = [all_addi_infos[addi_id]
                           for addi_id in addi_id_list]
        species.additional_infos = addi_infos_list


class Migration(migrations.Migration):

    dependencies = [
        ('species', 'import_g'),
    ]

    operations = [
        migrations.RunPython(populate_m2m_species_additionalinfo),
    ]
