from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from . import forms


class RegistrationView(CreateView):
    form_class = forms.RegistrationForm
    template_name = 'homepagetest.html'
    success_url = reverse_lazy('home:homepage')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            current_url = self.request.headers.get('Referer')
            data = {'success': False, 'errors': form.errors, 'status': 400, 'url': current_url}
            return JsonResponse(data)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            current_url = self.request.headers.get('Referer')
            data = {'success': True, 'status': 200, 'url': current_url}
            return JsonResponse(data)
        else:
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_register'] = self.get_form()
        return context


class UserLoginView(View):
    form_class = forms.UserLogin
    template_name = 'homepagetest.html'
    success_url = reverse_lazy('home:homepage')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form_login': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                current_url = self.request.headers.get('Referer')
                data = {'success': True, 'url': current_url}
                return JsonResponse(data)
        data = {'success': False, 'errors': form.errors}
        return JsonResponse(data)


def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('home:homepage'))




