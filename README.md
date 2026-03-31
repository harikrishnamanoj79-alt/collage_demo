# 🎓 Apex University — Django College Website

A cinematic full-stack college website built with **Django** + **GSAP** + **Lenis**.  
All content is managed via Django Admin. Zero external dependencies on the backend beyond Django + Pillow.

---

## ✨ Features

| Feature | Details |
|---|---|
| **CMS** | Full Django Admin panel — edit Hero, About, Blog, Gallery, contact messages |
| **Animations** | GSAP ScrollTrigger — parallax, reveals, counters, stagger, clip-path |
| **Smooth Scroll** | Lenis smooth scroll, integrated with GSAP ticker |
| **Dark Cinematic UI** | Playfair Display + DM Sans, gold accents, noise texture |
| **Preloader** | Animated progress bar preloader |
| **Custom Cursor** | Magnetic ring cursor (desktop only) |
| **Gallery** | Masonry grid + lightbox with keyboard/swipe navigation |
| **Blog** | List + detail pages, category filter, related posts |
| **Contact** | Form saves to DB, admin reads messages at /admin/ |
| **Responsive** | Fully mobile-responsive, hamburger menu |
| **Marquee** | Animated scrolling text strip |

---

## 🚀 Quick Start

### 1. Clone / extract the project

```bash
cd college_site
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Seed sample content (optional but recommended)

```bash
python manage.py seed_data
```

This creates sample Hero, About Us, and 3 Blog posts so the site isn't empty.

### 6. Create an admin superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 7. Run the development server

```bash
python manage.py runserver
```

### 8. Open in browser

| URL | Page |
|---|---|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/blog/ | Blog listing |
| http://127.0.0.1:8000/gallery/ | Gallery |
| http://127.0.0.1:8000/contact/ | Contact |
| http://127.0.0.1:8000/admin/ | **Admin panel** |

---

## 🗂 Project Structure

```
college_site/
├── college_site/               # Django project config
│   ├── settings.py             # All settings (DB, static, media)
│   ├── urls.py                 # Root URL routing
│   └── wsgi.py
│
├── core/                       # Main app
│   ├── models.py               # HeroSection, AboutUs, Blog, Gallery, ContactMessage, SiteSettings
│   ├── views.py                # Views for all pages
│   ├── urls.py                 # URL patterns
│   ├── admin.py                # Admin panel config
│   ├── forms.py                # Contact form
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py    # python manage.py seed_data
│   │
│   ├── templates/core/
│   │   ├── base.html           # Base layout (navbar, footer, scripts)
│   │   ├── home.html           # Home page with all sections
│   │   ├── blog_list.html      # Blog listing
│   │   ├── blog_detail.html    # Individual blog post
│   │   ├── gallery.html        # Full gallery
│   │   └── contact.html        # Contact page
│   │
│   └── static/core/
│       ├── css/main.css        # Full cinematic stylesheet
│       └── js/
│           ├── main.js         # Preloader, Lenis, GSAP, cursor, navbar
│           ├── home.js         # Lightbox + stat counters
│           └── gallery.js      # Gallery page lightbox
│
├── media/                      # Uploaded files (images/videos via admin)
├── requirements.txt
└── manage.py
```

---

## 🎨 Admin Guide

After logging into `/admin/`:

### Hero Section
- Go to **Core → Hero Sections → Add**
- Set **Title**, **Subtitle**, upload a **Background Image** or **Video**
- Mark **Is Active** = ✅ (only one should be active)

### About Us
- Go to **Core → About Us → Add**
- Fill in description, upload an image, set statistics (students, faculty, programs)

### Blog Posts
- Go to **Core → Blog Posts → Add**
- Set title — the **slug** auto-fills from it
- Add a **Featured Image**, **Excerpt** (preview text), and full **Content** (HTML supported)
- Toggle **Is Published** to show/hide

### Gallery
- Go to **Core → Gallery Images → Add**
- Upload images, add captions, set categories (e.g. Campus, Events, Sports)
- Use **Order** field to control display order

### Contact Messages
- Go to **Core → Contact Messages**
- Read-only view of all messages from the contact form
- Toggle **Is Read** to track which you've reviewed

### Site Settings
- Go to **Core → Site Settings → Add**
- Set college name, contact details, social media URLs

---

## 🧠 Animation Architecture

All animations live in `static/core/js/main.js`:

| Animation | Trigger | GSAP Method |
|---|---|---|
| Hero text reveal | Page load | `gsap.timeline()` with `clipPath` |
| Hero parallax | Scroll | `scrollTrigger` + `yPercent` scrub |
| Section reveals | Scroll into view | `gsap.to()` with `once: true` |
| Gallery images | Scroll | `stagger` + `scale` |
| Stat counters | Scroll into view | `gsap.to()` on `obj.val` |
| Blog cards | Scroll | `stagger` + `y` |
| Marquee | Always | Pure CSS `animation` |

---

## ⚙️ Customization

### Change college name/branding
- Admin → **Site Settings** — edit college name, logo, colors via CSS variables

### Change color scheme
Edit `static/core/css/main.css` CSS variables at the top:
```css
:root {
  --gold:  #c9a55a;   /* Change accent color */
  --black: #080808;   /* Change background */
  --white: #f4f0eb;   /* Change text color */
}
```

### Add PostgreSQL (optional)
In `settings.py`, replace the DATABASES block:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Then `pip install psycopg2-binary` and re-run migrations.

### Production deployment
1. Set `DEBUG = False` in settings.py
2. Change `SECRET_KEY` to a secure random key
3. Add your domain to `ALLOWED_HOSTS`
4. Run `python manage.py collectstatic`
5. Serve media/static with Nginx or WhiteNoise

### Deploy on Render
This repo includes [`render.yaml`](c:\Users\User\Downloads\college_website_django\college_site\render.yaml) and a deployment bootstrap command so the project can go to Render with the current SQLite data and current media files.

What is included:
- Production static handling with WhiteNoise
- Startup migration with `python manage.py migrate`
- `python manage.py bootstrap_site` to keep bundled media available and ensure the default admin account exists
- Default superuser login: `admin` / `admin`

Important note about current data:
- The current `db.sqlite3` and `media/` folder should be pushed with the repo so the existing content and hero video appear on first deploy.
- Render's default local filesystem is ephemeral, so future admin uploads, form submissions, and database changes can be lost on restart or redeploy unless you attach a persistent disk or move to PostgreSQL/object storage.

Render steps:
1. Push the project to GitHub or GitLab, including `db.sqlite3` and `media/`.
2. In Render, create a new Blueprint service from the repository.
3. Deploy with the generated `render.yaml`.
4. Open `/admin/` and sign in with `admin` / `admin`.
5. Change the admin password after first login.

Optional persistence:
- Set `SQLITE_PATH` to a mounted disk path if you add a Render persistent disk.
- Set `MEDIA_ROOT` to a mounted disk path if you want future uploads to stay after redeploys.
- If you later set `DATABASE_URL`, the app will use that database automatically.

---

## 📦 Dependencies

**Python / Backend**
- `Django >= 4.2` — web framework
- `Pillow >= 10.0` — image processing (required for ImageField)

**Frontend (CDN — no npm needed)**
- [GSAP 3.12](https://gsap.com/) — scroll animations
- [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) — scroll-based triggering
- [Lenis 1.0](https://github.com/studio-freight/lenis) — smooth scrolling
- [Google Fonts](https://fonts.google.com/) — Playfair Display + DM Sans + DM Mono

---

## 🛠 Common Issues

**Images not showing after upload**
→ Make sure `MEDIA_ROOT` and `MEDIA_URL` are set correctly in `settings.py`
→ In dev, Django serves media automatically via `urls.py` static() helper

**Animations not playing**
→ Check browser console for GSAP CDN errors
→ GSAP loads via CDN — ensure internet connection in dev

**Admin CSS missing**
→ Run `python manage.py collectstatic`

---

Built with ❤️ using Django 4.2 · GSAP 3.12 · Lenis 1.0
#   c o l l a g e _ d e m o  
 
#   c o l l a g e _ d e m o  
 