from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
import random


#First page the user sees. Lists entries and a search form.
def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
        "form": SearchForm()
    })


#Takes in a title (if exists) and renders its Markdown into html.
def entry(request, title):
    page = util.get_entry(title)
    if page == None:
        return render(request, "encyclopedia/error.html")
    
    html = markdown2.markdown(page)
    return render(request, "encyclopedia/entry.html", {
        "entry": html, 
        "title": title
    })


#Takes input from the search form and looks for the query.
def search(request):
    related_entries = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            entries = util.list_entries()
            for parser in entries:
                if query.lower() == parser.lower():
                    return redirect(reverse('entry', args=[query]))
            
            for parser in entries:
                if parser.lower().find(query.lower()) != -1:
                    related_entries.append(parser)
                    return render(request, "encyclopedia/query_results.html", {
                        "entries": related_entries
                    })
            return render(request, "encyclopedia/error.html")


#Creates a new encyclopedia entry. 
def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) != None:
                return render(request, "encyclopedia/error.html")
            else:
                util.save_entry(title, content)
                return redirect(reverse('entry', args=[title]))
    return render(request, "encyclopedia/new_entry.html", {
        "form1": NewEntryForm()
    })


#Allows the user to edit an existing entry.
def editEntry(request, title):
    content = util.get_entry(title)
    if content != None:
        form = NewEntryForm(initial={"content": content, "title": title})
        form.fields['title'].widget = forms.HiddenInput()
        return render(request, "encyclopedia/edit_entry.html", {
            "form2": form
        })


#Saving the edited entry to the disk.
def saveEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(reverse('entry', args=[title]))


#Takes the user to any random page. 
def randomPage(request):
    entries = util.list_entries()
    chosen_page = random.choice(entries)
    return redirect(reverse('entry', args=[chosen_page]))


class SearchForm(forms.Form):
    query = forms.CharField(label="Search")

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea())