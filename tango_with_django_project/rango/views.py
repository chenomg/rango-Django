from datetime import datetime
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, SearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from rango import bing_search


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)
    # response.set_cookie('visits', context_dict['visits'])
    return response


def search(request):
    if request.method == "POST":
        form = request.POST
        query = form['query'].strip()
        results = [{}]
        try:
            results = bing_search.run_query(query)
        except IOError:
            results[0]['title'] = 'bing.key file not found!'
        except KeyError:
            results[0]['title'] = 'key not found!'
        except Warning:
            results[0][
                'title'] = 'Search Error, check the key file and web connection!'
        context_dict = {'results': results, 'query': query}
    else:
        context_dict = None
    return render(request, 'rango/search.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
        if request.method == "POST":
            form = request.POST
            query = form['query'].strip()
            results = [{}]
            try:
                results = bing_search.run_query(query)
            except IOError:
                results[0]['title'] = 'bing.key file not found!'
            except KeyError:
                results[0]['title'] = 'key not found!'
            except Warning:
                results[0][
                    'title'] = 'Search Error, check the key file and web connection!'
            context_dict['results'] = results
            context_dict['query'] = query
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)


def about(request):
    if request.session.test_cookie_worked():
        print('Test Cookie worked!')
        request.session.delete_test_cookie()
    context_dict = {'yourname': 'Jase Chen'}
    print('request method:', request.method)
    print('Login User:', request.user)
    return render(request, 'rango/about.html', context=context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
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
    return render(
        request, 'rango/register.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered,
        })


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponse('Your rango account is disable.')
        else:
            print('Invalid login details: {}, {}'.format(username, password))
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse('Since you logged in you can see this page!')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit',
                                               str(datetime.now())[:-7])
    last_visit_time = datetime.strptime(last_visit_cookie, '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).seconds > 1:
        visits += 1
        request.session['last_visit'] = str(datetime.now())[:-7]
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits


def track_url(request, page_id):
    if request.method == 'GET':
        page = Page.objects.get(id=page_id)
        page.views += 1
        page.save()
        return HttpResponseRedirect(page.url)


def register_profile(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.save()
    return render(request, 'rango/profile_registration.html', {})
