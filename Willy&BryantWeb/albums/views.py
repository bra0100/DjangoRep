from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Album
from .forms import AlbumForm, CustomUserCreationForm




class AlbumListView(ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'
    paginate_by = 10

    def get_queryset(self):
        return Album.objects.all().order_by('-id')




class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/upload_album.html'

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.uploaded_by

    def form_valid(self, form):
        messages.success(
            self.request, f'Album "{form.instance.title}" successfully updated!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = True 
        return context



class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'albums/delete_album.html'

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.uploaded_by

    def delete(self, request, *args, **kwargs):
        album = self.get_object()
        messages.success(request, f'Album "{album.title}" has been deleted!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('album_list')




@login_required
def upload_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False, user=request.user)
            album.save()
            messages.success(
                request, f'Album "{album.title}" by {album.band} successfully added!')
            return redirect('album_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AlbumForm()

    return render(request, 'albums/upload_album.html', {'form': form})


class HomeView(TemplateView):
    template_name = 'albums/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['recent_albums'] = Album.objects.all().order_by('-id')[:3]
        context['total_albums'] = Album.objects.count()
        return context



def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})




def custom_logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(
            request, f'Goodbye, {username}! You have been logged out.')
    return redirect('home')




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 'Registration successful! Welcome to the Metal Archives.')
            return redirect('home')
        else:
            messages.error(request, 'Correct the errors below, dude.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
