"""
Django Admin configuration.
All content is manageable from the admin panel at /admin/
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HeroSection,
    AboutUs,
    Blog,
    Gallery,
    UpcomingEvent,
    ContactMessage,
    AdmissionInquiry,
    SiteSettings,
)


# ─── Custom Admin Site Header ────────────────────────────────────────────────
admin.site.site_header = "Apex University — Content Manager"
admin.site.site_title = "Apex University Admin"
admin.site.index_title = "Website Content Management"


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at', 'preview_bg')
    list_editable = ('is_active',)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'cta_text', 'cta_link')
        }),
        ('Background Media', {
            'fields': ('background_image', 'background_video'),
            'description': 'Upload either an image or video. Video takes priority if both are set.'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def preview_bg(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.background_image.url)
        return "—"
    preview_bg.short_description = "Preview"


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'tagline', 'description', 'image')
        }),
        ('Statistics', {
            'fields': ('founded_year', 'students_count', 'faculty_count', 'programs_count'),
            'description': 'Displayed as animated counters on the website.'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at', 'preview_image')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'slug', 'author', 'category', 'is_published')
        }),
        ('Content', {
            'fields': ('image', 'excerpt', 'content')
        }),
        ('Dates', {
            'fields': ('created_at',)
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return "—"
    preview_image.short_description = "Image"


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category', 'order', 'is_visible', 'uploaded_at', 'preview')
    list_editable = ('order', 'is_visible')
    list_filter = ('category', 'is_visible')
    search_fields = ('caption', 'category')

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.image.url)
        return "—"
    preview.short_description = "Preview"


@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'event_time', 'location', 'display_order', 'is_active')
    list_filter = ('is_active', 'category', 'event_date')
    list_editable = ('display_order', 'is_active')
    search_fields = ('title', 'summary', 'location', 'category')
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'category', 'summary')
        }),
        ('Schedule', {
            'fields': ('event_date', 'event_time', 'location', 'display_order')
        }),
        ('Action', {
            'fields': ('cta_text', 'cta_link', 'is_active')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'submitted_at')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_at')

    # Prevent adding messages from admin (they come from the contact form)
    def has_add_permission(self, request):
        return False


@admin.register(AdmissionInquiry)
class AdmissionInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'program_interest', 'is_reviewed', 'submitted_at')
    list_filter = ('is_reviewed', 'program_interest', 'submitted_at')
    search_fields = ('name', 'email', 'phone', 'city', 'program_interest')
    list_editable = ('is_reviewed',)
    readonly_fields = (
        'name', 'email', 'phone', 'city', 'program_interest',
        'current_qualification', 'message', 'submitted_at'
    )

    def has_add_permission(self, request):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity', {
            'fields': ('college_name', 'tagline', 'logo')
        }),
        ('Contact Info', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url')
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
    )

    def has_add_permission(self, request):
        # Only one SiteSettings object should exist
        return not SiteSettings.objects.exists()
