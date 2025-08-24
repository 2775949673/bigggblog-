from django.http import JsonResponse
from django.http.response import JsonResponse
from django.shortcuts import render,reverse,redirect
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST,require_GET
from .models import Blog,BlogComment,BlogCategory
from .forms import PubBlogForm
from django.db.models import Q



# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request, "index.html", context={"blogs":blogs})

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
        print(f"找到博客: {blog.id}, 标题: {blog.title}")  # 添加调试信息
        return render(request, "blog_detail.html", context={"blog": blog})
    except Exception as e:
        print(f"查找博客时出错: {e}")  # 添加调试信息
        blog = None
    return render(request, "blog_detail.html", context={"blog": blog})

@require_http_methods(['GET', 'POST'])
@login_required(login_url='/auth/login')  # 指定正确的登录URL
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={"categories": categories})
    else:
        print("收到POST请求，表单数据:", request.POST)  # 添加调试信息
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({"code": 200, "message": "博客发布成功！", "data": {"blog_id": blog.id}})
        else:
            print("表单验证失败:", form.errors)  # 添加详细错误信息
            # 返回更详细的错误信息
            error_messages = {}
            for field, errors in form.errors.items():
                error_messages[field] = [str(error) for error in errors]
            return JsonResponse({'code': 400, "message": "参数错误！", "errors": error_messages})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(blog_id=blog_id, content=content, author=request.user)
    #重新加载
    return redirect(reverse("blog:blog_detail",kwargs = {'blog_id':blog_id}))

@require_GET
def search(request):
    q = request.GET.get('q')
    if not q:
        return redirect('blog:index')
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request, 'index.html', context={"blogs": blogs})














