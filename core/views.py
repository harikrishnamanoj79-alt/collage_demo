"""
Views for the college website.
Each view fetches data from the database and renders the appropriate template.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import HeroSection, AboutUs, Blog, Gallery, UpcomingEvent, SiteSettings
from .forms import ContactForm, AdmissionInquiryForm


def get_site_settings():
    """Helper: fetch global site settings (used by all pages)."""
    return SiteSettings.objects.first()


def get_portal_content():
    """Shared content blocks for portal-style pages."""
    quick_links = [
        {'title': 'Apply Now', 'href': '/admissions/', 'description': 'Start your admission enquiry with the campus office.'},
        {'title': 'Upcoming Events', 'href': '/events/', 'description': 'See seminars, workshops, fests, and campus programs.'},
        {'title': 'Academics', 'href': '/academics/', 'description': 'Explore programs, learning pathways, and departments.'},
        {'title': 'Campus Life', 'href': '/campus-life/', 'description': 'Discover clubs, events, culture, and student experiences.'},
        {'title': 'Student Corner', 'href': '/student-corner/', 'description': 'Find student support highlights and useful resources.'},
        {'title': 'Contact Office', 'href': '/contact/', 'description': 'Reach admissions, administration, and support teams.'},
    ]
    programs = [
        {'name': 'B.Tech Programs', 'meta': 'Undergraduate', 'description': 'Career-focused engineering education with strong fundamentals and practical training.'},
        {'name': 'M.Tech Programs', 'meta': 'Postgraduate', 'description': 'Advanced specialization for students pursuing deeper technical expertise.'},
        {'name': 'Industry Readiness', 'meta': 'Career Development', 'description': 'Workshops, seminars, and placement-oriented activities that prepare students for recruitment.'},
        {'name': 'Student Clubs', 'meta': 'Campus Life', 'description': 'Technical, cultural, and service communities that build leadership beyond the classroom.'},
    ]
    campus_highlights = [
        {'title': 'Admissions Support', 'text': 'A clearer path for prospective students with direct enquiry and contact points.'},
        {'title': 'Academic Updates', 'text': 'Homepage access to current news, notices, and important institutional activity.'},
        {'title': 'Program Discovery', 'text': 'A dedicated section to help visitors understand courses and learning pathways quickly.'},
        {'title': 'Campus Experience', 'text': 'Gallery-driven storytelling that highlights life, events, and student achievements.'},
    ]
    academics_features = [
        {'title': 'Outcome-Based Learning', 'text': 'Structured teaching plans, strong fundamentals, and practical exposure across disciplines.'},
        {'title': 'Labs and Research', 'text': 'Hands-on sessions, project work, and faculty-guided research opportunities.'},
        {'title': 'Training and Placement', 'text': 'Interview readiness, skill development, and recruiter engagement throughout the year.'},
    ]
    campus_life = [
        {'title': 'Clubs and Communities', 'text': 'Technical clubs, cultural teams, volunteering groups, and leadership forums.'},
        {'title': 'Events and Festivals', 'text': 'Hackathons, symposiums, art festivals, sports meets, and annual celebrations.'},
        {'title': 'Mentoring Environment', 'text': 'Faculty support, peer learning, and a student-first campus atmosphere.'},
    ]
    student_corner = [
        {'title': 'Notice Board', 'text': 'A place for exam reminders, event alerts, and administrative updates.'},
        {'title': 'Career Resources', 'text': 'Resume guidance, aptitude support, placement readiness, and internship awareness.'},
        {'title': 'Help Desk', 'text': 'Fast access to admissions, academics, and student support contacts.'},
    ]
    departments = [
        {'title': 'Computer Science', 'text': 'Programming, AI foundations, software engineering, and digital systems.'},
        {'title': 'Mechanical Engineering', 'text': 'Manufacturing, design, thermal systems, and industrial problem-solving.'},
        {'title': 'Electronics and Communication', 'text': 'Embedded systems, communication networks, and modern electronics.'},
        {'title': 'Civil Engineering', 'text': 'Infrastructure, structural design, environmental systems, and planning.'},
    ]
    admissions_steps = [
        {'title': 'Choose Your Program', 'text': 'Compare the available undergraduate and postgraduate learning tracks.'},
        {'title': 'Send an Enquiry', 'text': 'Use the admission form to let the team know your interests and background.'},
        {'title': 'Receive Guidance', 'text': 'The admissions office follows up with eligibility, next steps, and support.'},
    ]
    student_services = [
        {'title': 'Academic Support', 'text': 'Mentoring, remediation support, and guidance for semester planning.'},
        {'title': 'Placement Preparation', 'text': 'Soft skills, aptitude training, resume workshops, and mock interviews.'},
        {'title': 'Wellbeing and Guidance', 'text': 'A healthier student experience through approachable support systems.'},
        {'title': 'Digital Access', 'text': 'Important announcements, resources, and learning updates in one place.'},
    ]
    return {
        'quick_links': quick_links,
        'programs': programs,
        'campus_highlights': campus_highlights,
        'academics_features': academics_features,
        'campus_life': campus_life,
        'student_corner': student_corner,
        'departments': departments,
        'admissions_steps': admissions_steps,
        'student_services': student_services,
    }


def home(request):
    """
    Home page — aggregates all sections:
    Hero, About, Blog (latest 3), Gallery (latest 8), Contact form.
    """
    hero = HeroSection.objects.filter(is_active=True).first()
    about = AboutUs.objects.filter(is_active=True).first()
    recent_blogs = Blog.objects.filter(is_published=True)[:3]
    gallery_images = Gallery.objects.filter(is_visible=True)[:8]
    upcoming_events = UpcomingEvent.objects.filter(is_active=True)[:4]
    contact_form = ContactForm()
    admission_form = AdmissionInquiryForm()
    site = get_site_settings()
    portal_content = get_portal_content()

    # Handle contact form submission (POST from same page)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'admission':
            admission_form = AdmissionInquiryForm(request.POST)
            if admission_form.is_valid():
                admission_form.save()
                messages.success(request, "Admission enquiry submitted successfully. Our team will contact you soon.")
                return redirect('home')
            messages.error(request, "Please correct the admission form errors below.")
        else:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, "Your message has been sent! We'll get back to you soon.")
                return redirect('home')
            messages.error(request, "Please correct the errors below.")

    context = {
        'hero': hero,
        'about': about,
        'recent_blogs': recent_blogs,
        'gallery_images': gallery_images,
        'upcoming_events': upcoming_events,
        'contact_form': contact_form,
        'admission_form': admission_form,
        'site': site,
        **portal_content,
        'page': 'home',
    }
    return render(request, 'core/home.html', context)


def blog_list(request):
    """
    Blog listing page — all published posts, paginated.
    """
    all_blogs = Blog.objects.filter(is_published=True)
    categories = Blog.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    site = get_site_settings()

    # Optional category filter via GET param
    category = request.GET.get('category', '')
    if category:
        all_blogs = all_blogs.filter(category=category)

    context = {
        'blogs': all_blogs,
        'categories': [c for c in categories if c],
        'active_category': category,
        'site': site,
        'page': 'blog',
    }
    return render(request, 'core/blog_list.html', context)


def blog_detail(request, slug):
    """
    Individual blog post page.
    """
    post = get_object_or_404(Blog, slug=slug, is_published=True)
    related = Blog.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    site = get_site_settings()

    context = {
        'post': post,
        'related': related,
        'site': site,
        'page': 'blog',
    }
    return render(request, 'core/blog_detail.html', context)


def gallery(request):
    """
    Gallery page — all visible images in a masonry/grid layout.
    """
    images = Gallery.objects.filter(is_visible=True)
    categories = Gallery.objects.filter(is_visible=True).values_list('category', flat=True).distinct()
    site = get_site_settings()

    # Optional category filter
    category = request.GET.get('category', '')
    if category:
        images = images.filter(category=category)

    context = {
        'images': images,
        'categories': [c for c in categories if c],
        'active_category': category,
        'site': site,
        'page': 'gallery',
    }
    return render(request, 'core/gallery.html', context)


def contact(request):
    """
    Standalone contact page.
    """
    site = get_site_settings()
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please fix the errors below.")

    context = {
        'form': form,
        'site': site,
        'page': 'contact',
    }
    return render(request, 'core/contact.html', context)


def events_page(request):
    site = get_site_settings()
    events = UpcomingEvent.objects.filter(is_active=True)
    context = {
        'events': events,
        'site': site,
        'page': 'events',
    }
    return render(request, 'core/events.html', context)


def admissions_page(request):
    site = get_site_settings()
    form = AdmissionInquiryForm()
    portal_content = get_portal_content()

    if request.method == 'POST':
        form = AdmissionInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admission enquiry submitted successfully. Our team will contact you soon.")
            return redirect('admissions')
        messages.error(request, "Please correct the admission form errors below.")

    context = {
        'form': form,
        'site': site,
        'page': 'admissions',
        'programs': portal_content['programs'],
        'admissions_steps': portal_content['admissions_steps'],
    }
    return render(request, 'core/admissions.html', context)


def academics_page(request):
    site = get_site_settings()
    portal_content = get_portal_content()
    context = {
        'site': site,
        'page': 'academics',
        'programs': portal_content['programs'],
        'academics_features': portal_content['academics_features'],
        'departments': portal_content['departments'],
    }
    return render(request, 'core/academics.html', context)


def campus_life_page(request):
    site = get_site_settings()
    portal_content = get_portal_content()
    gallery_images = Gallery.objects.filter(is_visible=True)[:8]
    recent_blogs = Blog.objects.filter(is_published=True)[:3]
    context = {
        'site': site,
        'page': 'campus_life',
        'campus_life': portal_content['campus_life'],
        'gallery_images': gallery_images,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'core/campus_life.html', context)


def student_corner_page(request):
    site = get_site_settings()
    portal_content = get_portal_content()
    recent_blogs = Blog.objects.filter(is_published=True)[:4]
    upcoming_events = UpcomingEvent.objects.filter(is_active=True)[:3]
    context = {
        'site': site,
        'page': 'student_corner',
        'student_corner': portal_content['student_corner'],
        'student_services': portal_content['student_services'],
        'recent_blogs': recent_blogs,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'core/student_corner.html', context)
