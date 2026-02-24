# Django Tips

## 1. **Understand the MTV Pattern**

Django uses **Model-Template-View** (not MVC):

- **Model**: Database structure (your data)
- **Template**: HTML presentation (what users see)
- **View**: Business logic (processes requests)

```python
# Model defines data
class Post(models.Model):
    title = models.CharField(max_length=200)

# View processes logic
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/list.html', {'posts': posts})

# Template displays data
# {{ post.title }}
```

## 2. **Always Use Virtual Environments**

Never install Django globally:

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install Django
pip install django
```

## 3. **Never Commit SECRET_KEY or Credentials**

Move secrets to environment variables:

```python
# settings.py
import os
from pathlib import Path

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-only')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Use .env files with python-decouple or django-environ
```

Add to `.gitignore`:

```
venv/
*.pyc
db.sqlite3
.env
```

## 4. **Migrations Are Your Friend**

Always create and run migrations after model changes:

```bash
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply to database

# Check migration status
python manage.py showmigrations
```

**Never** edit the database directly - use migrations!

## 5. **Use Django's Built-in Tools**

Don't reinvent the wheel:

```python
# Authentication - use Django's system
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    ...

# Forms - use Django forms
from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# Admin - register your models
from django.contrib import admin
admin.site.register(Post)
```

## 6. **Follow Django's Project Structure**

Organize properly from the start:

```
myproject/
├── manage.py
├── myproject/          # Project folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app1/               # App folder
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── app1/      # Namespace templates!
│   └── static/
│       └── app1/      # Namespace static files!
└── requirements.txt
```

## 7. **Use `get_object_or_404()`**

Instead of try/except for objects:

```python
# ❌ Don't do this
try:
    post = Post.objects.get(id=post_id)
except Post.DoesNotExist:
    return HttpResponse("Not found", status=404)

# ✅ Do this
from django.shortcuts import get_object_or_404
post = get_object_or_404(Post, id=post_id)
```

## 8. **Learn the QuerySet API**

Avoid N+1 queries with `select_related()` and `prefetch_related()`:

```python
# ❌ Bad - causes multiple queries
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # Additional query each time!

# ✅ Good - single query with JOIN
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.name)
```

## 9. **Use `{% url %}` Tag, Never Hardcode URLs**

```django
{# ❌ Bad #}
<a href="/blog/post/5/">View Post</a>

{# ✅ Good #}
<a href="{% url 'blog:post_detail' post.id %}">View Post</a>
```

In `urls.py`:

```python
app_name = 'blog'  # Namespace
urlpatterns = [
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
```

## 10. **Set DEBUG = False in Production**

```python
# settings.py
DEBUG = False  # In production!
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

Debug mode exposes sensitive information!

## 11. **Use Django's Class-Based Views**

Start with function views, but learn CBVs for common patterns:

```python
from django.views.generic import ListView, DetailView

class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 10
```

Much shorter than writing it all manually!

## 12. **Validate User Input**

Always use forms for validation:

```python
# views.py
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():  # Validates!
            form.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {'form': form})
```

## 13. **Use Django Shell for Testing**

Test queries and code interactively:

```bash
python manage.py shell

>>> from blog.models import Post
>>> Post.objects.all()
>>> Post.objects.create(title="Test")
```

## 14. **Read the Documentation**

Django has **excellent documentation**: <https://docs.djangoproject.com/>

When stuck, search: "django [what you want to do]"

## 15. **Common Beginner Mistakes to Avoid**

- ❌ Forgetting `{% csrf_token %}` in POST forms
- ❌ Not running migrations after model changes
- ❌ Using `python manage.py runserver` in production
- ❌ Storing media files in static folder
- ❌ Making database queries in templates
- ❌ Not using `get_absolute_url()` for model URLs
- ❌ Ignoring Django's security features

## 16. **Keep Requirements.txt Updated**

```bash
# Create/update requirements
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## 17. **Start Small, Then Refactor**

- Build one feature at a time
- Get it working first
- Then optimize and clean up
- Don't over-engineer initially

## Quick Workflow

```bash
# 1. Start project
django-admin startproject myproject
cd myproject

# 2. Create app
python manage.py startapp myapp

# 3. Add to INSTALLED_APPS in settings.py

# 4. Create models in models.py

# 5. Make migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

**Remember**: Django is designed to make web development easier. Use its built-in features rather than reinventing them!
