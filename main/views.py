from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ToDoList
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required

@login_required
def index(request, id):
    """
    View for displaying and managing a to-do list.

    Parameters:
    - request: HttpRequest object
    - id: Integer representing the id of the ToDoList to be displayed

    Returns:
    - Rendered HTML template displaying the to-do list
    """
    # Retrieve the ToDoList with the specified id
    ls = ToDoList.objects.get(id=id)
    
    # Check if the logged-in user has access to this specific list
    if ls not in request.user.todolist.all():
        return render(request, "main/list.html", {"ls": ls, "user_authenticated": request.user.is_authenticated})
    if request.method == "POST":
        # Process form submissions
        if request.POST.get("complete"):
            for item in ls.item_set.all():
                # Update completion status of items based on user input
                if request.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True    
                # else:
                #     item.complete = False
                item.save()
        # Process form submissions
        elif request.POST.get("delete"):
            for item in ls.item_set.all():
                # Update completion status of items based on user input
                if request.POST.get("c" + str(item.id)) == "clicked":
                        item.delete()
                    
        elif request.POST.get("newItem"):
            # Create a new item in the to-do list
            txt = request.POST.get("new")
            if len(txt) > 0:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("Invalid input")

    # Render the to-do list template
    return render(request, "main/list.html", {"ls": ls, "user_authenticated": request.user.is_authenticated})

def home(request):
    """
    View for rendering the home page.

    Parameters:
    - request: HttpRequest object

    Returns:
    - Rendered HTML template for the home page
    """
    return render(request, "main/home.html", {"user_authenticated": request.user.is_authenticated})

def create(request):
    """
    View for creating a new to-do list.

    Parameters:
    - request: HttpRequest object

    Returns:
    - Rendered HTML template for creating a new to-do list
    - Redirect to the newly created to-do list on successful form submission
    """
    if request.method == "POST":
        # Process form submissions for creating a new to-do list
        form = CreateNewList(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)
            
            return HttpResponseRedirect("/%i" % t.id)
    
    else:
        form = CreateNewList()

    # Render the create to-do list template
    return render(request, "main/create.html", {"form": form, "user_authenticated": request.user.is_authenticated})

def view(request):
    """
    View for rendering the page displaying all to-do lists.

    Parameters:
    - request: HttpRequest object

    Returns:
    - Rendered HTML template for viewing all to-do lists
    """
    return render(request, "main/view.html", {"user_authenticated": request.user.is_authenticated})
