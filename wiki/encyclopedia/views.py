# Imports
from django.shortcuts import render
from django import forms
from . import util
import random 
import markdown2

# Class to create a form to add an entry
class NewEntry(forms.Form):
    # title
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
            'class':'form-control', 'id':'input',
            'placeholder':'Enter title'
                 }))
    # content
    content = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control','id':'content',
            'rows':10,'cols':150,'placeholder':'Enter markdown content'
    }))
    
# index page list all enteries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

# Get entry by its title . If a match is found,returns its markdown content ,convert it into html using markdown_content function ,then displays it . 
# Otherwise  returns an no entry found response.
def getentry(request,title):
        markdowncontent = util.get_entry(title.lower())
        if markdowncontent:
            Content=markdown_content(markdowncontent)
            return render(request,"encyclopedia/entry.html",{
                "data":Content,
                "title":title
            }
            ) 
        else:
                            
            return render(request,"encyclopedia/response.html",{
               "response":" Error: No such entry exists❌"
            }
            )

# Function to convert markdown content to Html
def markdown_content(content):
     return markdown2.markdown(content)

# Function to add an entry
# if the entry already exists, the entry is not saved and returns an error response.
# Otherwise Saves the new entry
def addentry(request):

    if request.method=="POST":
        entry = NewEntry(request.POST)
    # if the file already exists,shows error response
        if entry.is_valid():
            title = entry.cleaned_data["title"]
            content = entry.cleaned_data["content"]
            if util.get_entry(title):
                return render(request,"encyclopedia/response.html",{
                     "response": " Error: Cannot add entry: Entry already exists❗"
                })
    #  adds new entry
            else:
                 util.save_entry(title,content)
                 return render(request,"encyclopedia/response.html",{
                     "response": "Entry Saved😊"
                })
                 
                 
                 
    else:
                
            new = NewEntry()
            return render(request,'encyclopedia/add.html',{
                "new":new

            })

# Opens a  Random entry
def randomentry(request):
     entry = random.choice(util.list_entries())
     return  getentry(request,entry)
# Searches for an entry . If an exact match is found, the entry is displayed,otherwise the matching search results ar displayed
def searchentry(request):
    result=[]
    if request.method=="POST":
        title = request.POST.get("q")
        markdowncontent=util.get_entry(title)
        if markdowncontent:
            htmlcontent= markdown_content(markdowncontent)
            return render(request,"encyclopedia/entry.html",{
                "data":htmlcontent
            }
            )
        else:
            enteries= util.list_entries()
            for list in enteries :
                if title.lower() in list.lower():
                    result.append(list) 
                    
            
            if not result:
                 return render(request,"encyclopedia/response.html",{
                      "response":"No result found"
                 })      
            else:
                 return render(request,"encyclopedia/search.html",{
                      "searchresult":result
                 })

# Edit an existing entry

def editentry(request):
    if request.method=="POST":
         title=request.POST.get("title")
         content =request.POST.get("content")
         util.save_entry(title,content)
         return render(request,"encyclopedia/response.html",{
              "response": "Changes saved😊"
         })
    else:
        title= request.GET.get("filename")
        content=util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title": title,
            "content":content
        })
     
               
          
     
          