from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import *
from datetime import datetime,date
import calendar
import json
import os

# homepage
def home_page(request):
    return render(request, 'common/home.html')

# lab member page
def people_page(request):
    # Get all lab members
    members = lab_member.objects.all()
    # Split members to render in different category
    pi = lab_member.objects.filter(title='Principal Investigator',alumni=False)
    staff = lab_member.objects.filter(title='Research Staff',alumni=False)
    postdoc = lab_member.objects.filter(title='Postdoc',alumni=False)
    gradstudent = lab_member.objects.filter(title='Graduate Student',alumni=False)
    ra = lab_member.objects.filter(title='Research Assistant',alumni=False)
    undergrad = lab_member.objects.filter(title='Undergraduate Student',alumni=False)
    other = members.exclude(alumni=True).difference(pi,staff,postdoc,gradstudent,ra,undergrad)
    alumni = lab_member.objects.filter(alumni=True)
    return render(request, 'common/people.html', {
        'pi': pi,
        'staff': staff,
        'postdoc': postdoc,
        'gradstudent': gradstudent,
        'ra': ra,
        'undergrad': undergrad,
        'other': other,
        'alumni': alumni,
        'members': members
        })

# research
def research_page(request):
    return render(request, 'common/research.html')

# publications
def publications_page(request):
    publications = publication.objects.all().order_by('-date')
    dateobjs = publication.objects.dates('date','year',order='DESC')
    years = [date.year for date in dateobjs]
    return render(request, 'common/publications.html',{'publications':publications,'years': years})

# news
def news_page(request):
    try:
        data = request.GET
        year = data['year']
        month = data['month']
    except:
        month = 'month'
        year = 'year'
    now = datetime.now()
    if year == 'year' and month == 'month': # get last 5 news items if main
        news = news_item.objects.all().order_by('-pub_date')[0:5]
    elif year == 'year':
        news = news_item.objects.filter(pub_date__month=int(month)).order_by('-pub_date')
        month = int(month)
    elif month == 'month':
        news = news_item.objects.filter(pub_date__year=int(year)).order_by('-pub_date')
        year = int(year)
    else:
        year = int(year)
        month = int(month)
        dayrange = calendar.monthrange(year,month)
        start_date = date(year,month,1)
        end_date = date(year,month,dayrange[1])
        news = news_item.objects.filter(pub_date__range=(start_date,end_date)).order_by('-pub_date')
    return render(request, 'common/news.html',{
        'news': news,
        'year': year,
        'month': month,
        'yearnum': range(2018,now.year+1),
        'monthnum': range(1,13)
        })

# data/software
def data_page(request):
    data = data_listing.objects.all().order_by('title')
    software = software_listing.objects.all().order_by('title')
    return render(request, 'common/data_software.html', {'data': data, 'software': software})

# directions/contact
def directions_page(request):
    return render(request, 'common/directions_contact.html')
