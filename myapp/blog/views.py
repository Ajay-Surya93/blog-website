from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post,AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm

# Create your views here.
# Static demo data
# posts = [
# {'id':1, 'title' : 'Post 1' , 'content' : 'Content from post1'},
# {'id':2, 'title' : 'Post 2' , 'content' : 'Content from post2'},
# {'id':3, 'title' : 'Post 3' , 'content' : 'Content from post3'},
# {'id':4, 'title' : 'Post 4' , 'content' : 'Content from post4'},
# ]

def index(request):
    blog_title = "Latest Post"
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts,5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    
    return render(request,"blog/index.html", {'blog_title' : blog_title , 'page_obj' : page_obj})

def detail(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404("Page Does Not Exist!")
    # post = next((item for item in posts if item['id'] == int(post_id)),None)
    # logger = logging.getLogger("TESTING")
    # logger.debug = (f"post variable is {post}")
    return render(request,"blog/detail.html",{'post' : post, 'related_post' : related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_url_page'))

def new_url_view(request):
    return HttpResponse("This is new URL")

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f"Post Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}")
            success_message = "Your mail is sent!"
            return render(request,"blog/contact.html",{"form":form,"success_message":success_message})
        else:
            logger.debug("Form invalid")
        return render(request,"blog/contact.html",{"form":form,"name":name,"email":email,"message":message})
    return render(request,"blog/contact.html")

def about_view(request):
    about_content = AboutUs.objects.first().content
    return render(request,"blog/about.html",{'about_content':about_content})