"""Species application admin"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Species, AdditionalInfo, SpeciesPhotos
from .forms import SpeciesForm, AdditionalInfoForm


class SpeciesPhotosInline(admin.TabularInline):
    """Inline Species Photos forms factory"""
    model = SpeciesPhotos
    max_num = 10


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    """Admin Species table"""
    list_display = ['latin_name', 'vernacular', 'genus', 'have_addi_info']
    ordering = ['latin_name']
    list_filter = ['genus']
    save_on_top = True
    search_fields = ['latin_name', 'genus__name', 'vernacular']
    form = SpeciesForm
    inlines = [
        SpeciesPhotosInline,
    ]
    fieldsets = (
        ('Crucial informations', {
            'fields': ('latin_name', 'genus')
        }),
        ('Add more informations', {
            'fields': ('additional_infos', 'vernacular', 'colour', 'nesting',
                       'queen_size', 'worker_size', 'polymorphism', 'male_size',
                       'female_size', 'minor_size', 'major_size'
                       )
        })
    )
    filter_vertical = ['additional_infos']


class AssignedFilter(admin.SimpleListFilter):
    """Custom Additional Info Admin filter showing all unassigned additional
    infromations
    """
    title = _('assignment')
    parameter_name = 'is_used'

    def lookups(self, request, model_admin):
        return (
            ('used', _('in use')),
            ('unused', _('unused'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'unused':
            return queryset.filter(species__isnull=True)
        elif self.value() == 'used':
            return queryset.filter(species__isnull=False).distinct()


@admin.register(AdditionalInfo)
class AdditionalInfoAdmin(admin.ModelAdmin):
    """Admin Additional Informations table"""
    list_display = ['info_key', 'info_value', 'assigned_to_species']
    ordering = ['info_key']
    list_filter = ['info_key', AssignedFilter]
    form = AdditionalInfoForm


@admin.register(SpeciesPhotos)
class SpeciesPhotosAdmin(admin.ModelAdmin):
    """Admin Species Photos table"""
    list_display = ['__str__', 'photo', 'photo_thumbnail']
    list_filter = ['species__genus__name']
    search_fields = ['species__latin_name', 'species__vernacular',
                     'species__genus__name']
