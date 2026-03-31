import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

from core.models import AboutUs, Blog, HeroSection, SiteSettings


class Command(BaseCommand):
    help = "Prepare the site for deployment by copying bundled media, seeding empty content, and ensuring a default superuser."

    def handle(self, *args, **options):
        self.copy_bundled_media()
        self.seed_if_empty()
        self.ensure_superuser()

    def copy_bundled_media(self):
        source_root = Path(settings.BUNDLED_MEDIA_ROOT)
        target_root = Path(settings.MEDIA_ROOT)

        if not source_root.exists():
            self.stdout.write("No bundled media directory found, skipping media sync.")
            return

        if source_root.resolve() == target_root.resolve():
            self.stdout.write("Bundled media and MEDIA_ROOT are the same path, skipping media sync.")
            return

        copied_files = 0
        for source_path in source_root.rglob('*'):
            if not source_path.is_file():
                continue

            relative_path = source_path.relative_to(source_root)
            target_path = target_root / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)

            if not target_path.exists():
                shutil.copy2(source_path, target_path)
                copied_files += 1

        self.stdout.write(self.style.SUCCESS(f"Media sync complete. Copied {copied_files} file(s)."))

    def seed_if_empty(self):
        has_content = any([
            SiteSettings.objects.exists(),
            HeroSection.objects.exists(),
            AboutUs.objects.exists(),
            Blog.objects.exists(),
        ])

        if has_content:
            self.stdout.write("Existing site content found, skipping seed data.")
            return

        call_command('seed_data')
        self.stdout.write(self.style.SUCCESS("Seed data created because the database was empty."))

    def ensure_superuser(self):
        username = getattr(settings, 'DEFAULT_SUPERUSER_USERNAME', None) or 'admin'
        password = getattr(settings, 'DEFAULT_SUPERUSER_PASSWORD', None) or 'admin'
        email = getattr(settings, 'DEFAULT_SUPERUSER_EMAIL', None) or 'admin@example.com'

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )

        updates = []
        if user.email != email:
            user.email = email
            updates.append('email')
        if not user.is_staff:
            user.is_staff = True
            updates.append('is_staff')
        if not user.is_superuser:
            user.is_superuser = True
            updates.append('is_superuser')

        user.set_password(password)
        updates.append('password')
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created default superuser '{username}'.")) 
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated default superuser '{username}' ({', '.join(updates)})."))
