from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from . forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from . models import Post
# Create your views here.


def home(request):

    posts = Post.objects.all()

    return render(request, "blog/home.html", {"post": posts, "active": "active"})


def about(request):
    return render(request, "blog/about.html", {"active": "active"})


def contact(request):

    return render(request, "blog/contact.html", {"active": "active"})


def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Post.objects.all()
        fn = user.get_full_name()
        gps = user.groups.all()

        return render(request, "blog/dashboard.html", {"post": posts, "fn": fn, "gps": gps})
    else:
        return HttpResponseRedirect('/ulogin/')


def ulogout(request):
    logout(request)
    return HttpResponseRedirect('/')


def ulogin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                un = form.cleaned_data['username']
                pa = form.cleaned_data['password']

                user = authenticate(username=un, password=pa)
                if user is not None:
                    login(request, user)
                    messages.success(request, "You Logged In Successfully")
                return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, "blog/login.html", {"form": form, "active": "active"})
    else:
        return HttpResponseRedirect('/dashboard/')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(
                request, "Congratulations!! You have became a Author Now!")
            user = form.save()
            group = Group.objects.get(name="Author")
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, "blog/signup.html", {"form": form, "active": "active"})


# Add a post using this function

def add(request, ):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
                messages.success(request, "New Post Added successfully")
            return render(request, "blog/addpost.html", {"form": form})
        else:
            form = PostForm()
        return render(request, "blog/addpost.html", {"form": form})

    else:
        return HttpResponseRedirect('/ulogin/')


def update(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Post is  Updated successfully")
                return render(request, "blog/updatepost.html", {"form": form})
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, "blog/updatepost.html", {"form": form})

    else:
        return HttpResponseRedirect('/ulogin/')


def delete(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                a = Post(id=id)
                a.delete()
                messages.success(request, "Post Deleted Successfully!")
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponse("You Cannot Delete like this, Please use the Delete button")
        else:
            return HttpResponse("<h2>You are not allowed to Access this page </h2>")

    else:
        return HttpResponseRedirect('/ulogin/')
