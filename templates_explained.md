# Django templates

 are regular HTML files with special syntax that gets processed on the server
 before being sent to the browser. There are three key pieces of syntax, all
 visible in your project:

1. Variables: {{ }}
Double curly braces output a value from the context — the dictionary passed by
the view.

In your view (render(request, "blog/index.html", {"posts": posts})), the key
 "posts" becomes available in the template as {{ posts }}. You can access attributes with dot notation:

{{ post.title }} — accesses the title field
{{ post.author }} — accesses the author field
{{ post.pk }} — accesses the primary key
2. Tags: {% %}
Curly-brace-percent signs execute logic — loops, conditionals, URL resolution,
etc.

From your index.html:

{% for post in posts %} — loops over the queryset
{% empty %} — runs if the list is empty (like an else for the loop)
{% endfor %} — closes the loop
{% url 'blog:post_detail' post.pk %} — reverses a named URL pattern, generating
 a path like /blog/3/
3. Filters: |
Filters transform a variable's output. In your detail.html:

{{ post.article|linebreaks }} — converts plain-text newlines into <p> and <br>
HTML tags

How the flow works
A request comes in (e.g. blog)
The view (post_list) queries the database and calls render(), passing a
template path and a context dict ({"posts": posts})
Django's template engine loads index.html, replaces all {{ }} and {% %} with
real values, and returns plain HTML
The browser receives normal HTML — no Django syntax is visible to the user
Template discovery
Django finds templates because APP_DIRS: True is set in settings. It looks
inside each app's templates/ folder. The extra blog subdirectory (index.html)
is a namespace convention to avoid collisions if multiple apps have a template
named index.html.
