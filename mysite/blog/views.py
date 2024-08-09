from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForms
from django.core.mail import send_mail

# def post_list(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)    
#     except EmptyPage:
#         # Если page_number находится вне диапазона, то
#         # выдать последнюю страницу
#         posts = paginator.page(paginator.num_pages)    
#     return render(request, 'blog/post/list.html', {'posts': posts})

def post_share(request, post_id):
    #Извлечь пост по индитификатору  
    post = get_object_or_404(Post,
                            id=post_id,
                            status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        #Форма отправлена на обработку
        form = EmailPostForms(request.POST)
        if form.is_valid():
            #Поля формы прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} рекомендуем тебе прочитать'\
                      f'{post.title}'
            message = f'Читатйте {post.title} в {post_url}\n\n'\
                      f'{cd["name"]} комментарии: {cd["comments"]}'
            send_mail(subject, message, 'nikitamikhailov2392@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForms()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})            

           
class PostListView(ListView):
    queryset = Post.objects.all()
    content_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)    
    return render(request,
                  'blog/post/detail.html',
                   {'post': post})

