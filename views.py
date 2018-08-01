"""Species application views"""
from django.shortcuts import render

from .models import Species


def show_single_species(request, latin_name):
    """Show chosen species"""

    try:
        chosen_species = Species.objects.get(latin_name=latin_name)

    except Exception as error:
        error_details = '{}'.format(error)
        ctx = {'error': error_details}
        return render(request, 'species/single_species.html', ctx)

    # Save chosen species latin name
    chosen_species_latin_name = chosen_species.latin_name

    # Adding basic species info
    print(chosen_species.vernacular)
    chosen_species_data = {
        'Nazwa zwczajowa': chosen_species.vernacular,
        'Rodzaj': chosen_species.genus.name,
        'Nazwa łacińska': chosen_species.latin_name,
        'Kolor': chosen_species.colour,
        'Zakładanie gniazd': chosen_species.nesting,
        'Wielkość królowej': chosen_species.queen_size,
        'Wielkość robotnic': chosen_species.worker_size,
        'Polimorfizm': chosen_species.polymorphism,
        'Wielkość samca': chosen_species.male_size,
        'Wielkość samicy': chosen_species.female_size,
        'Najmniejsze': chosen_species.minor_size,
        'Największe': chosen_species.major_size
    }
    # Deleting values with empty string or None
    chosen_species_data =\
        {k: v for k, v in chosen_species_data.items()
         if v != '' and v is not None}

    # Adding additional info
    chosen_species_addi_infos = chosen_species.additional_infos.all()
    chosen_species_addi_infos_data = {}
    for additional_info in chosen_species_addi_infos:
        chosen_species_addi_infos_data[additional_info.info_key] = \
            additional_info.info_value

    # Adding species photos and photos thumbnails urls
    chosen_species_photos = chosen_species.speciesphotos_set.all()
    chosen_species_photos_data = []
    for photo_object in chosen_species_photos:
        chosen_species_photos_data.append({
            'photo_url': photo_object.photo.url,
            'thumbnail_url': photo_object.photo_thumbnail.url
        })

    # Adding similar species latin names and their main photos
    same_genus_species = \
        Species.objects.filter(genus__name=chosen_species.genus.name)\
        .exclude(latin_name=chosen_species.latin_name)
    similar_species_latin_names_and_photos = []
    for similar_species in same_genus_species[:3]:
        try:
            photo_url = similar_species.speciesphotos_set.all()[0].photo.url
        except IndexError:
            photo_url = ''
        similar_species_latin_names_and_photos.append({
            'latin_name': similar_species.latin_name,
            'photo_url': photo_url
        })

    ctx = {'chosen_species_latin_name': chosen_species_latin_name,
           'chosen_species_data': chosen_species_data,
           'chosen_species_addi_infos_data':
               chosen_species_addi_infos_data,
           'chosen_species_photos_data': chosen_species_photos_data,
           'similar_species_latin_names_and_photos':
               similar_species_latin_names_and_photos,
           }
    return render(request, 'species/single_species.html', ctx)
