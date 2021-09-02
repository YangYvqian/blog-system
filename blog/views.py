from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from . import models
import markdown
import pygments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def make_paginator(objects, page, num=10):
    paginator = Paginator(objects, num)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return object_list, paginator


def pagination_data(paginator, page):
    if paginator.num_pages == 1:
        return {}
    left = []
    right = []
    left_has_more = False
    right_has_more = False
    first = False
    last = False
    try:
        page_number = int(page)
    except ValueError:
        page_number = 1
    except:
        page_number = 1
    total_pages = paginator.num_pages
    page_range = paginator.page_range
    if page_number == 1:
        right = page_range[page_number:page_number+4]
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    else:
        left = page_range[(page_number-3) if (page_number - 3) > 0 else 0:page_number-1]
        right = page_range[page_number:page_number+2]

        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True
    data = {
        'left': left,
        'right':right,
        'left_has_more':left_has_more,
        'right_has_more':right_has_more,
        'first':first,
        'last':last,
    }
    return data


def index(request):
    entries = models.Entry.objects.all()
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def detail(request, blog_id):
    # entry = models.Entry.objects.get(id=blog_id)
    # 如果id存在就返回正确页面，否则返回404页面
    entry = get_object_or_404(models.Entry, id=blog_id)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    entry.body = md.convert(entry.body)
    entry.toc =md.toc
    entry.increase_visiting()
    return render(request, 'blog/detail.html', locals())


def category(request, category_id):
    categy = get_object_or_404(models.Category, id=category_id)
    # categy = models.Category.objects.get(id=category_id)
    entries = models.Entry.objects.filter(category=categy)
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def tags(request, tag_id):
    tag = get_object_or_404(models.Tag, id=tag_id)
    # tag =models.Tag.objects.get(id=tag_id)
    if tag.name == '全部':
        entries = models.Entry.objects.all()
    else:
        entries = models.Entry.objects.filter(tags=tag)
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def search(request):
    keyword = request.GET.get('keyword',None)
    if not keyword:
        error_msg = "请输入关键字"
        return render(request, 'blog/index.html', locals())

    entries = models.Entry.objects.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword))
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def archives(request, year, month):
    entries = models.Entry.objects.filter(created_time__year=year, created_time__month=month)
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def permission_denied(request, exception, template_name='blog/403.html'):
    return render(request, template_name, locals())


def page_not_found(request, exception, template_name='blog/404.html'):
    return render(request, template_name, locals())


def server_error(exception):
    return render("blog/500.html", status=500)




