from django.shortcuts import render, redirect, HttpResponse
from apps.page_break.models import *
import re

DATE_REGEX=re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')

def index(request):
    users=User.objects.all()
    num_pages=int(len(users)/20)
    if(len(users)%20!=0):
        num_pages+=1
    pages=[]
    for i in range(1, num_pages+1):
        pages.append(i)
    context={
        'users':users,
        'pages':pages
        }
    context['users']=context['users'][0:20]
    return render(request, 'page_break/pageBreak.html', context)

def processSearch(request):
    if(request.method!='POST'):
        print('Invalid entry attempt')
        return HttpResponse('Stop what you are doing')
    context={}
    search_words=request.POST['search_name'].split()
    if(len(search_words)==1):
        search_words.append('')
    if(len(request.POST['search_name'])==0):
        if(len(request.POST['from'])==0 and len(request.POST['to'])==0):
            context['users']=User.objects.all()
        elif(DATE_REGEX.match(request.POST['from']) and not DATE_REGEX.match(request.POST['to'])):
            context['users']=User.objects.filter(created_at__gte=request.POST['from'])
        elif(not DATE_REGEX.match(request.POST['from']) and DATE_REGEX.match(request.POST['to'])):
            context['users']=User.objects.filter(created_at__lte=request.POST['to'])
        elif(DATE_REGEX.match(request.POST['from']) and DATE_REGEX.match(request.POST['to'])):
            context['users']=User.objects.filter(created_at__lte=request.POST['to'], created_at__gte=request.POST['from'])

    elif(len(request.POST['from'])==0 and len(request.POST['to'])==0):
        context['users']=User.objects.filter(first_name__startswith=search_words[0], last_name__startswith=search_words[1])|User.objects.filter(email__startswith=search_words[0])|User.objects.filter(last_name__startswith=search_words[0])
    elif(DATE_REGEX.match(request.POST['from']) and not DATE_REGEX.match(request.POST['to'])):
        context['users']=User.objects.filter(first_name__startswith=search_words[0], last_name__startswith=search_words[1],created_at__gte=request.POST['from'])|User.objects.filter(email__startswith=search_words[0], created_at__gte=request.POST['from'])|User.objects.filter(last_name__startswith=search_words[0], created_at__gte=request.POST['from'])
    elif(not DATE_REGEX.match(request.POST['from']) and DATE_REGEX.match(request.POST['to'])):
        context['users']=User.objects.filter(first_name__startswith=search_words[0], last_name__startswith=search_words[1],created_at__lte=request.POST['to'])|User.objects.filter(email__startswith=search_words[0], created_at__lte=request.POST['to'])|User.objects.filter(last_name__startswith=search_words[0], created_at__lte=request.POST['to'])
    elif(DATE_REGEX.match(request.POST['from']) and DATE_REGEX.match(request.POST['to'])):
        context['users']=User.objects.filter(first_name__startswith=search_words[0], last_name__startswith=search_words[1],created_at__lte=request.POST['to'], created_at__gte=request.POST['from'])|User.objects.filter(email__startswith=search_words[0], created_at__lte=request.POST['to'], created_at__gte=request.POST['from'])|User.objects.filter(last_name__startswith=search_words[0], created_at__lte=request.POST['to'], created_at__gte=request.POST['from'])
    
    page_num=int(request.POST['page_num'])
    context['users']=context['users'][(page_num-1)*20:page_num*20]
    
    return render(request, 'page_break/users.html', context)

