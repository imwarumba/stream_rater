from django.shortcuts import render, redirect, reverse
from stream.models import Category, Streamer, UserProfile, User, Comment, SubComment
from stream.forms import UserProfileForm, UserForm, CommentForm, SubCommentForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from stream.webhose_search import run_query

'''
def search(request):
    result_list = []
    query = None
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Webhose search function to get the results list!
            result_list = run_query(query)
    return render(request, 'stream/search.html', {'result_list': result_list, 'search_query': query})
'''


def homepage(request):
    '''
    request.session.set_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    context_dict['last_visit'] = request.session['last_visit'].split('.')[0]
    '''

    context_dict = {}
    context_dict['categories'] = Category.objects.all()
    context_dict['streamers'] = Streamer.objects.all()
    response = render(request, 'stream/homepage.html', context=context_dict)
    return response


def about(request):
    context_dict = {}
    print("about accessed")
    return render(request, 'stream/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        streamers = Streamer.objects.filter(category=category)
        context_dict['streamers'] = streamers

        context_dict['category'] = category
        context_dict['query'] = category.name

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['streamers'] = None

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list

    return render(request, 'stream/category.html', context_dict)

def add_comment(request, name='', category_name_slug=''):
    context_dict = {}
    streamer = Streamer.objects.get(name=name)
    context_dict['streamer'] = streamer
    context_dict['slug'] = category_name_slug
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.streamer = streamer
            comment_form.user_name = request.user.username
            comment_form.rating = request.POST.get('rating')
            comment_form.text = request.POST.get('text')
            comment_form.save()
            return redirect(reverse('stream:show_streamer',
                                    kwargs={'name': name,
                                            'category_name_slug': category_name_slug, }))
    context_dict['form'] = form
    return render(request, 'stream/add_comment.html', context_dict)

def add_sub_comment(request,  id=0, name='', category_name_slug=''):
    context_dict = {}
    father_comment = Comment.objects.get(id=id, streamer__name=name)
    context_dict['id'] = id
    context_dict['name'] = name
    context_dict['slug'] = category_name_slug
    form = SubCommentForm()
    if request.method == 'POST':
        form =  SubCommentForm(request.POST)
        if form.is_valid():
            sub_comment_form = form.save(commit=False)
            sub_comment_form.father_comment = father_comment
            sub_comment_form.user_name = request.user.username
            sub_comment_form.text = request.POST.get('text')
            sub_comment_form.save()
            return redirect(reverse('stream:show_streamer',
                                    kwargs={'name': name,
                                            'category_name_slug': category_name_slug,}))
    context_dict['form'] = form
    return render(request, 'stream/add_sub_comment.html', context_dict)


def show_streamer(request, name='', category_name_slug=''):
    context_dict = {}
    streamer = Streamer.objects.get(name=name)
    category = Category.objects.get(slug=category_name_slug)
    comments = Comment.objects.filter(streamer=streamer)
    context_dict['comments'] = comments
    context_dict['streamer'] = streamer
    context_dict['category'] = category

    sub_comments = []
    num_of_comments = 0
    total_rating = 0
    for comment in comments:
        num_of_comments += 1
        total_rating += comment.rating
        sub_comments.append(SubComment.objects.filter(father_comment=comment))
    if num_of_comments == 0:
        streamer.rating = 0
    else:
        streamer.rating = round(total_rating / num_of_comments, 2)

    context_dict['sub_comments'] = sub_comments

    return render(request, 'stream/streamer.html', context_dict)

def comment_posted(request):
    return render(request, 'stream/comment_posted.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)#changed
        profile_form = UserProfileForm(request.POST)#changed

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    ctx = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered}

    return render(request, 'stream/register.html', context=ctx)


def user_login(request):
    error = None
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('homepage'))
            else:
                error = "Your account is disabled."

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            error = "Invalid login details supplied."

    return render(request, 'stream/login.html', {'error': error})


@login_required
def restricted(request):
    return render(request, 'stream/restricted.html', context={})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))

'''
# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


# Updated the function definition

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def track_url(request):
    streamer_id = None
    if request.method == 'GET':
        if 'streamer_id' in request.GET:
            streamer_id = request.GET['streamer_id']
            try:
                page = Streamer.objects.get(id=streamer_id)
                page.views = page.views + 1
                page.last_visit = timezone.now()

                print(page.views)
                page.save()
                return redirect(page.url)
            except Category.DoesNotExist:
                pass
        return redirect('homepage')

'''
@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('homepage')
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'stream/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('homepage')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({
        # 'website': userprofile.website,
        'picture': userprofile.picture
    })

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if form.is_valid():
            form.save(commit=True)

            return redirect('profile', user.username)

        else:

            print(form.errors)

    return render(request, 'stream/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})

'''
@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    return render(request, 'stream/list_profiles.html',
                  {'userprofile_list': userprofile_list})


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    return render(request, 'stream/cats.html', {'cats': cat_list})
'''
