# Checklist: Adding a `feedback` app to the `djas` project

---

## Stage 1 — Scaffold the app

**Command:** Run `python manage.py startapp feedback` from the project root.

This creates the `feedback/` directory with these auto-generated files:

| File | Purpose |
|---|---|
| `__init__.py` | Makes it a Python package (leave empty) |
| `apps.py` | App configuration class — will contain `FeedbackConfig` with `name = 'feedback'` |
| `models.py` | Empty, ready for your model |
| `views.py` | Empty, ready for your view functions |
| `admin.py` | Empty, ready for admin registration |
| `tests.py` | Empty, ready for tests |
| `migrations/__init__.py` | Empty init for the migrations package |

You also need to **manually create** these, which `startapp` does not generate:

| File to create | Purpose |
|---|---|
| `feedback/urls.py` | App-level URL routing |
| `feedback/forms.py` | Your `ModelForm` for the feedback form |
| `feedback/templates/feedback/feedback_form.html` | The single-page form template |

---

## Stage 2 — Register the app

**File:** `arrivingskills/settings.py` (around line 33–41)

**Change:** Add `'feedback.apps.FeedbackConfig'` to the `INSTALLED_APPS` list, following the same pattern as the existing `'blog.apps.BlogConfig'` entry.

---

## Stage 3 — Define the model

**File:** `feedback/models.py`

**Change:** Define a `Feedback` model class inheriting from `models.Model`. Typical fields for a customer feedback form might include:

- `name` — `CharField` for the customer's name
- `email` — `EmailField` for contact
- `message` — `TextField` for the feedback content
- `rating` — `IntegerField` or `PositiveSmallIntegerField` (e.g. 1–5)
- `created_at` — `DateTimeField(auto_now_add=True)` for the submission timestamp

Add a `__str__` method (the blog app returns `self.title`; here you'd return something like the name or a truncated message).

---

## Stage 4 — Create and run the migration

**Commands (two steps):**

1. `python manage.py makemigrations feedback` — generates `feedback/migrations/0001_initial.py` describing the new table.
2. `python manage.py migrate` — applies it to `db.sqlite3`, creating the `feedback_feedback` table.

---

## Stage 5 — Define the form

**File:** `feedback/forms.py` (you create this)

**Change:** Define a `FeedbackForm` class inheriting from `forms.ModelForm`, with an inner `class Meta` that sets:

- `model = Feedback`
- `fields` — list the fields the user should fill in (e.g. `["name", "email", "message", "rating"]`)

This follows the exact same pattern as `BlogPostForm` in `blog/forms.py`.

---

## Stage 6 — Write the view

**File:** `feedback/views.py`

**Change:** Define a single view function (e.g. `feedback_form`) that:

- On **GET**: instantiates an empty `FeedbackForm()` and renders the template.
- On **POST**: instantiates `FeedbackForm(request.POST)`, calls `form.is_valid()`, saves, and either redirects to a success URL or re-renders with errors.

This mirrors the `post_create` view in `blog/views.py`. You may also want a small thank-you response after successful submission (either a redirect to a separate thank-you template, or just re-render the form page with a success message).

---

## Stage 7 — Create the app-level URLs

**File:** `feedback/urls.py` (you create this)

**Change:** Define:

- `app_name = "feedback"` — enables namespacing (same pattern as `blog/urls.py`)
- A `urlpatterns` list with one or two paths:
  - `path("", views.feedback_form, name="feedback_form")` — the form page
  - Optionally a `path("thanks/", ...)` for a thank-you page

---

## Stage 8 — Wire into the project URLs

**File:** `arrivingskills/urls.py` (around line 21–25)

**Change:** Add a new entry to `urlpatterns`:

```python
path("feedback/", include("feedback.urls")),
```

This sits alongside the existing `path("blog/", include("blog.urls"))` line. The feedback form will then be accessible at `/feedback/`.

---

## Stage 9 — Create the template

**File:** `feedback/templates/feedback/feedback_form.html` (you create the full directory path)

**Change:** Create an HTML page following the same structure as `blog/templates/blog/create.html`:

- Standard HTML boilerplate (`<!doctype html>`, `<head>`, `<body>`)
- A `<form method="post">` containing:
  - `{% csrf_token %}` — required for POST forms
  - `{{ form.as_p }}` — renders each field in a `<p>` tag
  - A submit button
- Optionally display a success message using Django's messages framework or a context variable

---

## Stage 10 — Register in admin

**File:** `feedback/admin.py`

**Change:** Register the `Feedback` model so submissions are viewable in the Django admin. Follow the pattern from `blog/admin.py`:

- Import the model
- Use `@admin.register(Feedback)` decorator on a `FeedbackAdmin` class
- Set `list_display` to show useful columns (e.g. `name`, `email`, `rating`, `created_at`)
- Optionally set `search_fields`, `list_filter`, or `readonly_fields`

---

## Summary of all touched files

| File | Action |
|---|---|
| `feedback/__init__.py` | Auto-generated (leave empty) |
| `feedback/apps.py` | Auto-generated (no changes needed) |
| `feedback/models.py` | Define `Feedback` model |
| `feedback/forms.py` | **Create** — define `FeedbackForm` ModelForm |
| `feedback/views.py` | Define `feedback_form` view function |
| `feedback/urls.py` | **Create** — define `app_name` and `urlpatterns` |
| `feedback/admin.py` | Register `Feedback` model |
| `feedback/tests.py` | Auto-generated (add tests when ready) |
| `feedback/migrations/` | Auto-generated by `makemigrations` |
| `feedback/templates/feedback/feedback_form.html` | **Create** — the form template |
| `arrivingskills/settings.py` | Add to `INSTALLED_APPS` |
| `arrivingskills/urls.py` | Add `path("feedback/", ...)` |
