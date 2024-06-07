from django.contrib import admin

from advertisements.models import Advertisement, FeaturedAds


class FeaturedAdsInline(admin.TabularInline):
    model = FeaturedAds
    extra = 1


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'creator',
                    'created_at', 'updated_at']
    inlines = [FeaturedAdsInline]

