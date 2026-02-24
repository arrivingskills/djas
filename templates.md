# Django Templates Quick Guide

## What Are Django Templates?

Django templates are text files that define the structure and layout of your HTML pages. They use Django's template language to dynamically generate content.

## Template Syntax Basics

### Variables

Use double curly braces to output variables:

```django
{{ variable_name }}
{{ user.username }}
{{ post.title }}
```

### Tags

Use curly brace-percent for control flow and logic:

```django
{% if user.is_authenticated %}
    Welcome, {{ user.username }}!
{% else %}
    Please log in.
{% endif %}

{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% endfor %}
```

### Filters

Transform variables using the pipe symbol:

```django
{{ post.title|lower }}
{{ post.created_at|date:"Y-m-d" }}
{{ content|truncatewords:30 }}
{{ text|default:"No text available" }}
```

## Template Location

Templates should be placed in one of these locations:

1. **App-level templates**: `app_name/templates/app_name/template_name.html`
   - Example: `blog/templates/blog/index.html`

2. **Project-level templates**: Configure in `settings.py`:

   ```python
   TEMPLATES = [
       {
           'DIRS': [BASE_DIR / 'templates'],
           ...
       }
   ]
   ```

## Using Templates in Views

### Function-Based Views

```python
from django.shortcuts import render

def my_view(request):
    context = {
        'title': 'My Page',
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/index.html', context)
```

### Class-Based Views

```python
from django.views.generic import ListView

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
```

## Template Inheritance

### Base Template (`base.html`)

```django
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    <header>
        {% block header %}
            <h1>My Website</h1>
        {% endblock %}
    </header>
    
    <main>
        {% block content %}
        {% endblock %}
    </main>
    
    <footer>
        {% block footer %}
            <p>&copy; 2026 My Site</p>
        {% endblock %}
    </footer>
</body>
</html>
```

### Child Template

```django
{% extends 'base.html' %}

{% block title %}Blog Posts{% endblock %}

{% block content %}
    <h2>Recent Posts</h2>
    {% for post in posts %}
        <article>
            <h3>{{ post.title }}</h3>
            <p>{{ post.content|truncatewords:50 }}</p>
        </article>
    {% endfor %}
{% endblock %}
```

## Common Template Tags

### `{% url %}`

Generate URLs from view names:

```django
<a href="{% url 'blog:index' %}">Home</a>
<a href="{% url 'blog:detail' post.id %}">{{ post.title }}</a>
```

### `{% include %}`

Include another template:

```django
{% include 'blog/partials/post_card.html' %}
```

### `{% csrf_token %}`

Required for POST forms:

```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

### `{% load static %}`

Load static files:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

## Common Filters

- `{{ value|length }}` - Get length of a string or list
- `{{ text|lower }}` - Convert to lowercase
- `{{ text|upper }}` - Convert to uppercase
- `{{ text|title }}` - Title case
- `{{ date|date:"F d, Y" }}` - Format date
- `{{ number|floatformat:2 }}` - Format float to 2 decimals
- `{{ html|safe }}` - Mark as safe HTML (use carefully!)
- `{{ list|join:", " }}` - Join list with separator

## Working with Forms

### Render a Form

```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}  {# or form.as_table, form.as_ul #}
    <button type="submit">Submit</button>
</form>
```

### Manual Form Rendering

```django
<form method="post">
    {% csrf_token %}
    
    {% for field in form %}
        <div class="form-group">
            {{ field.label_tag }}
            {{ field }}
            {% if field.help_text %}
                <small>{{ field.help_text }}</small>
            {% endif %}
            {% for error in field.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        </div>
    {% endfor %}
    
    <button type="submit">Submit</button>
</form>
```

## Template Comments

```django
{# Single line comment #}

{% comment %}
Multi-line comment
Can span multiple lines
{% endcomment %}
```

## Context Processors

Context processors add variables to every template. Common built-in ones:

- `{{ request }}` - The current request object
- `{{ user }}` - The current user
- `{{ perms }}` - User permissions
- `{{ messages }}` - Flash messages

## Best Practices

1. **Use template inheritance** - Create a base template and extend it
2. **Keep logic in views** - Templates should focus on presentation
3. **Name templates clearly** - Use descriptive names like `post_list.html`
4. **Use the `{% url %}` tag** - Don't hardcode URLs
5. **Escape user input** - Django does this by default; only use `|safe` when necessary
6. **Organize templates by app** - Keep app templates in `app/templates/app/`
7. **Use context processors** - For data needed on every page
8. **Create reusable components** - Use `{% include %}` for repeated elements

## Quick Example: Complete Blog Post Template

```django
{% extends 'blog/base.html' %}
{% load static %}

{% block title %}{{ post.title }} - My Blog{% endblock %}

{% block content %}
    <article class="post-detail">
        <header>
            <h1>{{ post.title }}</h1>
            <p class="meta">
                By {{ post.author.username }} on {{ post.created_at|date:"F d, Y" }}
            </p>
        </header>
        
        <div class="post-content">
            {{ post.content|linebreaks }}
        </div>
        
        {% if post.tags.all %}
            <div class="tags">
                {% for tag in post.tags.all %}
                    <span class="tag">{{ tag.name }}</span>
                {% endfor %}
            </div>
        {% endif %}
        
        <footer>
            <a href="{% url 'blog:index' %}">← Back to all posts</a>
        </footer>
    </article>
{% endblock %}
```

## Resources

- [Official Django Templates Documentation](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Template Language Reference](https://docs.djangoproject.com/en/stable/ref/templates/language/)
- [Built-in Template Tags and Filters](https://docs.djangoproject.com/en/stable/ref/templates/builtins/)
