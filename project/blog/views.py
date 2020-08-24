from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger

# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 1) # По 3 статьи на каждой странице.
#     page = request.GET.get('page')
#     try:
#         posts = paginator.get_page(page)
#     except PageNotAnInteger:
#         # Если страница не является целым числом, возвращаем первую страницу.
#         posts = paginator.get_page(1)
#     return render(request,'list.html', {'page': page, 'posts': posts})

from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'list.html'

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'detail.html', {'post': post})

from .forms import EmailPostForm
from django.core.mail import send_mail

def post_share(request, post_id):
    # Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # ... Отправка электронной почты.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you reading '{post.title}'"
            message = f"Read '{post.title}' at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 'form': form, 'sent': sent})