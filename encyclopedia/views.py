from django.http.response import HttpResponse
from django.shortcuts import render,redirect
import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getContent(request,title):
    storetitle = title
    if util.get_entry(title):
        text = util.get_entry(title)
        html = markdown.markdown(text)
    
        return render(request,"encyclopedia/entries.html",{
        "title" : html,
        "entrytitle" : title
        })
    else:
        return render(request,"encyclopedia/error.html",{
            
            "entrytitle" : title
        })

def search(request):
    value = request.GET.get('q','')
    if util.get_entry(value) is not None:
       return HttpResponseRedirect(reverse("title",kwargs={'title':value})) 
    else:
        subString = []
        for title in util.list_entries():
            if value.upper() in title.upper():
                subString.append(title)
        
        return render(request,"encyclopedia/index.html",{
            "entries" : subString,
            "search" : True,
            "value" :value
        })

def createNewPage(request):
    
    if request.method == "POST":
        tit =  request.POST.get('filename')
        cont = request.POST.get('contents')
        for entry in util.list_entries():
            if tit == entry:
                return render(request,"encyclopedia/create.html",{
                    "error" : "Can't add this page"
                })
            else:
                util.save_entry(tit,cont)
                return HttpResponseRedirect(reverse("index"))

    return render(request,"encyclopedia/create.html",{

    })
    
def edit(request,heading):
    content = util.get_entry(heading)

    if request.method == "POST":
        content = request.POST.get("contents")
        util.save_entry(heading,content)
        return HttpResponseRedirect(reverse("title",kwargs={'title':heading}))
        
    return render(request,"encyclopedia/edit.html",{
       "heading" : heading,
       "content" : content
    })

def rand(request):
    container = []
    for title in util.list_entries():
        container.append(title)
    
    stop = len(container)
    return HttpResponseRedirect(reverse("title",kwargs={'title':container[random.randint(0,stop-1)]}))