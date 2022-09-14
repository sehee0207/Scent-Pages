from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from accounts.forms import *
from django import forms
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, PasswordChangeView as AuthPasswordChangeView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordContextMixin
from django.urls import reverse_lazy
from .models import Accounts
from flask import request
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('photo:index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


# @login_required
def username_change(request):
    if request.method == 'POST': 
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('photo:mylist')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/username_change_form.html", {"form" : form})

class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    # reverse_lazy는 CBV에서 사용하는 reverse 함수이다.
    success_url = reverse_lazy("accounts:password_change")
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    # CBV에서도 form 객체를 사용할 수 있다.
    # form_valid 하다면 아래 함수가 실행된다.
    def form_valid(self, form):
        super().form_valid(form)
        return redirect('photo:mylist')
password_change = PasswordChangeView.as_view()

class Profile(CreateView):
    model = Accounts
    fields = ['profile_img']
    template_name_suffix = '_profile'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})