from django.http import HttpResponse
from django.shortcuts import render


# Главная страница
def index(request):
    template = 'posts/index.html'
    title = 'Это главная страница проекта Yatube'
    context = {
        'title': title,
        }
    return render(request, template, context) 


# def index(request):    
#     return HttpResponse('Главная страница')


# Страница со списком мороженого
def group_posts(request):
    return HttpResponse('Список мороженого')

# Главная страница
def group_posts(request):
    template = 'posts/group_list.html'
    title = 'Здесь будет информация о группах проекта Yatube'
    context = {
        'title': title,
        }
    return render(request, template, context)

