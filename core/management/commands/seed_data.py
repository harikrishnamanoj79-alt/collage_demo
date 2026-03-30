"""
Management command: python manage.py seed_data
Creates sample content so the website is not empty on first run.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import HeroSection, AboutUs, Blog, SiteSettings


class Command(BaseCommand):
    help = 'Seed the database with sample content for all sections'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with sample content...\n')

        # ─── Site Settings ────────────────────────────────
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                college_name="Apex University",
                tagline="Excellence · Innovation · Impact",
                footer_text="© Apex University. All rights reserved.",
                phone="+1 (800) 555-0100",
                email="info@apexuniversity.edu",
                address="1 University Avenue, Knowledge City, CA 94000",
                instagram_url="https://instagram.com",
                linkedin_url="https://linkedin.com",
                twitter_url="https://twitter.com",
            )
            self.stdout.write(self.style.SUCCESS('  ✓ SiteSettings created'))
        else:
            self.stdout.write('  – SiteSettings already exists, skipping')

        # ─── Hero Section ─────────────────────────────────
        if not HeroSection.objects.exists():
            HeroSection.objects.create(
                title="Shaping Minds,\nBuilding Futures",
                subtitle=(
                    "A world-class institution committed to academic excellence, "
                    "cutting-edge research, and transformative student experiences "
                    "that prepare graduates for a rapidly evolving world."
                ),
                cta_text="Explore Now",
                cta_link="#about",
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS('  ✓ HeroSection created'))
        else:
            self.stdout.write('  – HeroSection already exists, skipping')

        # ─── About Us ─────────────────────────────────────
        if not AboutUs.objects.exists():
            AboutUs.objects.create(
                title="About Apex University",
                tagline="Where curiosity meets excellence.",
                description=(
                    "<p>Apex University has stood at the forefront of higher education "
                    "for nearly four decades. Our commitment to rigorous scholarship, "
                    "interdisciplinary research, and holistic student development "
                    "has produced leaders who shape industries and communities worldwide.</p>"
                    "<p>With a diverse faculty of internationally recognized scholars and "
                    "state-of-the-art research facilities, we offer an environment where "
                    "intellectual curiosity flourishes and ambitions are realized.</p>"
                ),
                founded_year="1985",
                students_count="12000",
                faculty_count="680",
                programs_count="90",
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS('  ✓ AboutUs created'))
        else:
            self.stdout.write('  – AboutUs already exists, skipping')

        # ─── Blog Posts ───────────────────────────────────
        sample_posts = [
            {
                "title": "Apex Research Team Wins National Science Grant",
                "category": "Research",
                "excerpt": "Our interdisciplinary team secured a $4.2M federal grant to advance climate modeling research.",
                "content": (
                    "<p>The Department of Environmental Sciences at Apex University announced today "
                    "that a research team led by Professor Maya Chen has been awarded a $4.2 million "
                    "federal grant from the National Science Foundation.</p>"
                    "<h2>About the Research</h2>"
                    "<p>The five-year project, titled 'Next-Generation Climate Modeling Using AI,' "
                    "will develop machine learning tools to improve the precision of long-range "
                    "climate predictions — a challenge that has stumped researchers for decades.</p>"
                    "<p>The team includes collaborators from MIT, Stanford, and three European "
                    "universities, making this one of the most ambitious international climate "
                    "science projects in the institution's history.</p>"
                    "<h2>What This Means for Students</h2>"
                    "<p>Graduate students enrolled in the Climate Science and Data Engineering "
                    "programs will have the opportunity to participate directly in the research, "
                    "gaining hands-on experience with cutting-edge methodologies.</p>"
                ),
                "author": "Communications Office",
            },
            {
                "title": "Annual Cultural Fest 2025: A Celebration of Diversity",
                "category": "Events",
                "excerpt": "Over 5,000 students from 60 countries came together for our biggest cultural celebration yet.",
                "content": (
                    "<p>This year's Cultural Fest was nothing short of spectacular. Students from "
                    "over 60 countries transformed the Main Quad into a vibrant tapestry of music, "
                    "dance, food, and art — celebrating the extraordinary diversity that defines "
                    "the Apex community.</p>"
                    "<p>Highlights included a global food festival, live performances spanning "
                    "traditional Indian classical dance to West African drumming, and an art "
                    "installation that drew hundreds of photographs from the campus community.</p>"
                    "<h2>Voices from the Fest</h2>"
                    "<p>'Events like this remind me why I chose Apex,' said third-year student "
                    "Amara Diallo, who organized the West African pavilion. 'We don't just "
                    "coexist — we genuinely celebrate each other's stories.'</p>"
                    "<p>The annual festival, now in its 18th year, continues to grow as a "
                    "centerpiece of campus life and a testament to the university's global character.</p>"
                ),
                "author": "Student Affairs",
            },
            {
                "title": "New Centre for Artificial Intelligence Inaugurated",
                "category": "Campus",
                "excerpt": "Apex opens a state-of-the-art AI research hub with 200+ GPU servers and collaborative labs.",
                "content": (
                    "<p>The inauguration of the Apex Centre for Artificial Intelligence marks a "
                    "landmark moment in the university's 40-year journey. The 15,000 sq ft facility "
                    "houses over 200 high-performance GPU servers, collaborative research labs, "
                    "and a dedicated startup incubation space.</p>"
                    "<p>Speaking at the ceremony, Vice Chancellor Dr. James O'Brien said: "
                    "'This centre positions Apex at the intersection of industry and academia, "
                    "creating an ecosystem where the next generation of AI researchers and "
                    "entrepreneurs will be born.'</p>"
                    "<h2>Industry Partnerships</h2>"
                    "<p>The centre has already secured research partnerships with three Fortune 500 "
                    "companies and two government agencies, ensuring that the work happening here "
                    "addresses real-world challenges in healthcare, logistics, and public policy.</p>"
                ),
                "author": "Admin Office",
            },
        ]

        for post_data in sample_posts:
            slug = slugify(post_data['title'])
            if not Blog.objects.filter(slug=slug).exists():
                Blog.objects.create(
                    title=post_data['title'],
                    slug=slug,
                    category=post_data['category'],
                    excerpt=post_data['excerpt'],
                    content=post_data['content'],
                    author=post_data['author'],
                    is_published=True,
                )
                self.stdout.write(self.style.SUCCESS(f'  ✓ Blog post: "{post_data["title"][:40]}..."'))
            else:
                self.stdout.write(f'  – Blog post already exists: {slug}')

        self.stdout.write('\n' + self.style.SUCCESS(
            '✅ Database seeded successfully!\n\n'
            'Next steps:\n'
            '  1. Run: python manage.py createsuperuser\n'
            '  2. Run: python manage.py runserver\n'
            '  3. Visit: http://127.0.0.1:8000/\n'
            '  4. Admin:  http://127.0.0.1:8000/admin/\n'
        ))
