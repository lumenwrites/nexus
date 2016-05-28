from math import floor

# CBVs
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

# Models
from .models import Post
from .utils import rank_hot, check_if_rational, check_if_daily
from core.models import Util
from profiles.models import User
from hubs.models import Hub
from comments.models import Comment



class FilterMixin(object):
    paginate_by = 15
    def get_queryset(self):
        qs = super(FilterMixin, self).get_queryset()

        # Filter Stories
        qs = qs.filter(post_type="story")

        # Filter by site
        if check_if_rational(self.request):
            qs = qs.filter(rational=True)            

        if check_if_daily(self.request):
            qs = qs.filter(rational=True)            

        if not check_if_rational(self.request) and not  check_if_daily(self.request):
            qs = qs.filter(daily=False)
            
        # Filter by hubs
        try:
            selectedhubs = self.request.GET['hubs'].split(",")
        except:
            selectedhubs = []
        filterhubs = []
        if selectedhubs:
            for hubslug in selectedhubs:
                filterhubs.append(Hub.objects.get(slug=hubslug))
        for hub in filterhubs:
            qs = qs.filter(hubs=hub)            


        # Filter by query
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(Q(title__icontains=query) |
                           Q(body__icontains=query) |
                           Q(author__username__icontains=query))                    

        # Sort
        # (Turns queryset into the list, can't just .filter() later
        sorting = self.request.GET.get('sorting')
        if sorting == 'top':
            qs = qs.order_by('-score')
        elif sorting == 'new':
            qs = qs.order_by('-pub_date')
        else:
            qs = rank_hot(qs)

        return qs

    def get_context_data(self, **kwargs):
        context = super(FilterMixin, self).get_context_data(**kwargs)
        urlstring = ""
        # Sorting
        if self.request.GET.get('sorting'):
            sorting = self.request.GET.get('sorting')
        else:
            sorting = "hot"
        context['sorting'] = sorting

        # urlstring = self.request.path + "?sorting=" + sorting
            

        # Filtered Hubs
        try:
            selectedhubs = self.request.GET['hubs'].split(",")
        except:
            selectedhubs = []
        filterhubs = []
        if selectedhubs:
            for hubslug in selectedhubs:
                filterhubs.append(Hub.objects.get(slug=hubslug))
        context['filterhubs'] = filterhubs
        # All Hubs
        context['hubs'] = Hub.objects.all()
        # Solo Hub
        context['hub'] = self.request.GET.get('hub')


        if filterhubs:
            hublist = ",".join([hub.slug for hub in filterhubs])
            urlstring += "&hubs=" + hublist

        # Query
        query = self.request.GET.get('query')
        if query:
            context['query'] = query
            urlstring += "&query=" + query            

        context['urlstring'] = urlstring

        return context
    



class BrowseView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(BrowseView, self).get_queryset()        
        qs = [p for p in qs if (p.published == True and
                                p.author.approved ==True)]

        return qs


#     def get_context_data(self, **kwargs):
#         context = super(PostsView, self).get_context_data(**kwargs)
#         context['rankby'] =  self.kwargs['rankby']
#         return context    
    

class UserprofileView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(UserprofileView, self).get_queryset()

        # Filter by user
        userprofile = User.objects.get(username=self.kwargs['username'])        
        qs = [p for p in qs if (p.author==userprofile)]
        
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserprofileView, self).get_context_data(**kwargs)
        userprofile = User.objects.get(username=self.kwargs['username'])        
        context['userprofile'] = userprofile

        view_count = 0
        for post in userprofile.posts.all():
            view_count += post.views
        if view_count > 1000:
            view_count = str(floor(view_count/1000)) + "K"
        context['view_count'] = view_count
                
        score = 0        
        for post in userprofile.posts.all():
            score += post.score
        if score > 1000:
            score = str(int(score/1000)) + "K"
        context['score'] = score
        
        return context    
    

class SubscriptionsView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(SubscriptionsView, self).get_queryset()
        
        # Filter by subscriptions
        user = self.request.user
        subscribed_to = []
        if user.is_authenticated():
            subscribed_to = self.request.user.subscribed_to.all()
        
        qs = [p for p in qs if (p.author in subscribed_to)]
        
        return qs
        


# class HubView(FilterMixin, ListView):
#     model = Post
#     context_object_name = 'posts'    
#     template_name = "posts/browse.html"

#     def get_queryset(self):
#         qs = super(HubView, self).get_queryset()

#         # Filter by hub
#         hub = self.request.GET.get('hub')
#         hub = Hub.objects.get(slug=hub)
#         qs = [p for p in qs if (hub in p.hubs.all())]
        
#         return qs
        
        

# class PostView(DetailView):
#     model = Post
#     template_name = "posts/post.html"    

# class PostCreate(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = "posts/create.html"    

# class PostEdit(UpdateView): #form
#     template_name = "posts/edit.html"    
#     form_class = PostForm

#     success_url = '/thanks/'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.send_email()
#         return super(ContactView, self).form_valid(form)    



class HubList(ListView):
    model = Hub
    template_name = "hubs/hubs.html"


class SeriesList(ListView):
    model = Post
    template_name = "series/series.html"
    paginate_by=15
    



