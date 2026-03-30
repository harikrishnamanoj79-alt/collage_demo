"""
Models for the college website.
All content is admin-editable via Django Admin panel.
"""

from django.db import models
from django.utils import timezone


class HeroSection(models.Model):
    """
    Hero section content — fullscreen landing area.
    Admin can upload a background image or video, and set title/subtitle.
    Only ONE active hero section is shown at a time.
    """
    title = models.CharField(max_length=200, help_text="Main headline shown on hero")
    subtitle = models.TextField(help_text="Supporting text below the title")
    background_image = models.ImageField(
        upload_to='hero/', blank=True, null=True,
        help_text="Upload a fullscreen background image (JPG/PNG recommended)"
    )
    background_video = models.FileField(
        upload_to='hero/videos/', blank=True, null=True,
        help_text="Upload a background video (MP4). Video takes priority over image if both set."
    )
    cta_text = models.CharField(max_length=100, default="Explore Now", help_text="Call-to-action button text")
    cta_link = models.CharField(max_length=200, default="#about", help_text="CTA button target link")
    is_active = models.BooleanField(default=True, help_text="Only one hero section should be active")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return f"Hero: {self.title}"


class AboutUs(models.Model):
    """
    About Us section content.
    Admin can edit the college description, stats, and image.
    """
    title = models.CharField(max_length=200, default="About Our Institution")
    tagline = models.CharField(max_length=300, blank=True, help_text="Short bold tagline")
    description = models.TextField(help_text="Main about us description (supports HTML)")
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    founded_year = models.CharField(max_length=10, blank=True, help_text="e.g. 1985")
    students_count = models.CharField(max_length=20, blank=True, help_text="e.g. 12,000+")
    faculty_count = models.CharField(max_length=20, blank=True, help_text="e.g. 500+")
    programs_count = models.CharField(max_length=20, blank=True, help_text="e.g. 80+")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title


class Blog(models.Model):
    """
    Blog posts — dynamically listed and individually viewable.
    """
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, help_text="URL-friendly identifier (auto or manual)")
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short preview text for listing page")
    content = models.TextField(help_text="Full blog post content (supports HTML)")
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.CharField(max_length=100, default="Admin")
    category = models.CharField(max_length=100, blank=True, help_text="e.g. Events, Research, Campus Life")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog_detail', kwargs={'slug': self.slug})


class Gallery(models.Model):
    """
    Photo gallery — grid layout with lightbox on frontend.
    """
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=100, blank=True, help_text="e.g. Campus, Events, Sports")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    is_visible = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.caption or f"Gallery Image #{self.pk}"


class UpcomingEvent(models.Model):
    """
    Upcoming events shown on the home page.
    Admin can publish campus activities, seminars, and admission drives.
    """
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, help_text="e.g. Workshop, Seminar, Fest")
    event_date = models.DateField()
    event_time = models.CharField(max_length=100, blank=True, help_text="e.g. 10:00 AM - 1:00 PM")
    location = models.CharField(max_length=200, blank=True)
    summary = models.TextField(max_length=400, help_text="Short event description for the home page")
    cta_text = models.CharField(max_length=80, blank=True, default="Learn More")
    cta_link = models.CharField(max_length=200, blank=True, help_text="Optional internal or external link")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'event_date', 'title']
        verbose_name = "Upcoming Event"
        verbose_name_plural = "Upcoming Events"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """
    Messages submitted via the contact form.
    Admin can view/reply to these in the admin panel.
    """
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False, help_text="Mark as read once reviewed")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} <{self.email}>"


class AdmissionInquiry(models.Model):
    """
    Admission enquiries submitted from the home page.
    """
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=120, blank=True)
    program_interest = models.CharField(max_length=150)
    current_qualification = models.CharField(max_length=150, blank=True)
    message = models.TextField(blank=True)
    is_reviewed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Admission Inquiry"
        verbose_name_plural = "Admission Inquiries"

    def __str__(self):
        return f"Admission inquiry from {self.name}"


class SiteSettings(models.Model):
    """
    Global site settings — college name, logo, social links, footer text.
    """
    college_name = models.CharField(max_length=200, default="Apex University")
    tagline = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    footer_text = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.college_name
