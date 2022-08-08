from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect as redirect
from django.http import QueryDict
import markdown2 as md
from django.core.files.storage import default_storage
from django.http import JsonResponse
import random


def index(request):
    return render(request, "index.html", {
        "entries": util.list_entries()
    })


#Entry page should display content of encyclopedia entry
def target_page(request, id):
    
#process request
    
    if request.method == "GET":

    #Get content using util function
        if not util.get_entry(id):
            return False
                        
    #convert page to html
        content = md.markdown(util.get_entry(id))
        return render(request, "display.html", {
            "id" : id, 
            "content" : content
        })

        
    else:
        return render(request, "index.html", {
        "entries": util.list_entries()
        })
#Searches for entry in wikipedia
def search(request):

    if request.method != 'GET': 
        return None

    #Create list of entries
    if request.GET.get('q', '') == None:
        return None
    inpu = request.GET.get('q', '').lower().strip()
    items = util.list_entries()
    items = map(lambda x: x.lower(), items)
    new_list = []
    for item in items:
        if inpu in item:
            new_list.append(item)
        
    return JsonResponse({"items": new_list})

 
#Create page with a title form and 'textarea' and instructions on how to create in Markdown
def create_page(request):

    if request.method != 'GET':
        inpu = request.POST.get("textfield")
        title = request.POST.get("text")
        util.save_entry(title, inpu)
        return render(request, "success.html")
    return render(request, "create_page.html")
#Save feature

#Prompt user with error if page exists

#Render new page
    return render(request)

#Edit page's markdown using textarea
def edit_page(request):
    if request.method !="GET":
        title = request.POST.get("text")
        content = util.get_entry(title)
        return render(request, "create_page.html", {
            "title" : title,
            "content" : content
        })
#Prepopulate Textarea with current entry data

#Save feature

#Render new page
    return render(request, "edit_page.html")

def random_page(request):
    if request.method !="POST":
        content = util.list_entries()
        random_number = random.randint(0, len(content))
        random_content = content[random_number]
        return target_page(request, random_content)

    
