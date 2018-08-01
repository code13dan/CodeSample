"""Species application models"""
from django.db import models
from django.core.files import File

from string import ascii_letters, digits
from random import choices
from PIL import Image
from io import BytesIO


class Species(models.Model):
    """Species basic informations table"""
    vernacular = models.CharField(max_length=100, blank=True)
    latin_name = models.CharField(max_length=100, unique=True)
    colour = models.CharField(max_length=100, blank=True)
    nesting = models.CharField(max_length=100, blank=True)
    queen_size = models.CharField(max_length=15, blank=True)
    worker_size = models.CharField(max_length=15, blank=True)
    polymorphism = models.NullBooleanField()
    male_size = models.CharField(max_length=15, blank=True)
    female_size = models.CharField(max_length=15, blank=True)
    minor_size = models.CharField(max_length=15, blank=True)
    major_size = models.CharField(max_length=15, blank=True)
    additional_infos = models.ManyToManyField('AdditionalInfo', blank=True)
    genus = models.ForeignKey('genus.Genus', null=True,
                              on_delete=models.SET_NULL)

    @property
    def have_addi_info(self):
        """Check if species have assigned additional informations"""
        number_of_addi_infos = self.additional_infos.all().count()
        if number_of_addi_infos:
            return number_of_addi_infos
        else:
            return 'NO'

    def __str__(self):
        return self.latin_name

    class Meta:
        verbose_name_plural = 'Species'


class AdditionalInfo(models.Model):
    """Species additional informations table"""
    info_key = models.CharField(max_length=100)
    info_value = models.TextField()

    def __str__(self):
        """Callable name consist of additional information key and
        part of it's value, altogether length: 70 characters
        """
        brief_addi_info = '{} : {}'.format(self.info_key, self.info_value)
        if len(brief_addi_info) > 70:
            return brief_addi_info[:70] + '...'
        else:
            return brief_addi_info

    @property
    def assigned_to_species(self):
        """Check if additinal information is assigned to species"""
        number_of_assigned_species = self.species_set.all().count()
        if number_of_assigned_species:
            return number_of_assigned_species
        else:
            return 'NO'

    class Meta:
        verbose_name = 'Additinal informations'
        verbose_name_plural = 'Additional informations'


class SpeciesPhotos(models.Model):
    """Species photos table"""
    species = models.ForeignKey('Species', on_delete=models.SET_NULL,
                                blank=True, null=True)

    PHOTO_PATH_AND_NAME = ''
    THUMBNAIL_PATH_AND_NAME = ''

    def create_names_and_paths(self):
        """Create paths and names for species photo and thumbnail"""
        genus_name = self.species.genus.name.replace(' ', '_')
        species_latin_name = self.species.latin_name.replace(' ', '_')

        bad_luck = True
        while bad_luck:
            hashing = ''.join(choices(ascii_letters + digits, k=6))
            new_name = '{}_{}'.format(species_latin_name, hashing)
            bad_luck = SpeciesPhotos.objects.filter(
                photo__contains=new_name).exists()

        photo_new_name_and_path = 'user_images/{}/{}/{}.jpg'.format(
            genus_name, species_latin_name, new_name)
        thumbnail_new_name_and_path = \
            'user_images/{}/{}/{}_thumbnail.jpg'.format(
                genus_name, species_latin_name, new_name)

        self.PHOTO_PATH_AND_NAME = photo_new_name_and_path
        self.THUMBNAIL_PATH_AND_NAME = thumbnail_new_name_and_path

    def set_photo_name_and_path(instance, filename):
        """Assigned created thumbnail path and name"""
        return instance.PHOTO_PATH_AND_NAME

    photo = models.ImageField(upload_to=set_photo_name_and_path)

    def set_thumbnail_name_and_path(instance, filename):
        """Assigned created thumbnail path and name"""
        return instance.THUMBNAIL_PATH_AND_NAME

    photo_thumbnail = models.ImageField(upload_to=set_thumbnail_name_and_path,
                                        editable=False)

    def create_thumbnail(self):
        """Create thumbnail from uploaded image"""
        virtual_photo = BytesIO(self.photo.read())
        try:
            image = Image.open(virtual_photo)
            thumbnail_size = (80, 80)
            image.thumbnail(thumbnail_size)
            virtual_photo.close()
            virtual_thumbnail = BytesIO()
            image.save(virtual_thumbnail, 'JPEG')
        except IOError:
            print('image IO error')

        thumb_django_file_instance = File(virtual_thumbnail)
        self.photo_thumbnail.save(name='temporary.jpeg',
                                  content=thumb_django_file_instance,
                                  save=False)

        thumb_django_file_instance.close()
        virtual_thumbnail.close()

    def save(self, *args, **kwargs):
        self.create_names_and_paths()
        self.create_thumbnail()
        super().save(*args, **kwargs)

    def __str__(self):
        """Callable name consists of photo's species and genus names"""
        return 'photo-{}({})'.format(
            self.species.latin_name,
            self.species.genus.name)

    class Meta:
        verbose_name = 'Species photo'
        verbose_name_plural = 'Species photos'
