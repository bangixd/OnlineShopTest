from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserVerifyCodeForm, UserLoginForm
import random
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from datetime import datetime


class UserRegistrationView(View):

    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session['user_register_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'fullname': form.cleaned_data['fullname'],
                'password': form.cleaned_data['password']
            }
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            messages.success(request, 'we sen u a code', 'info')
            return redirect('account:user_verify')
        return render(request ,'account/register.html', {'form': form})


class UserRegisterVerifyView(View):
    form_class = UserVerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'account/verify.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        if form.is_valid():
            code_time = code_instance.created
            remaining_time = (datetime.now() - code_time.replace(tzinfo=None)).seconds
            if remaining_time > 120:
                messages.error(request, 'code expired try again', 'danger')
                code_instance.delete()
                return redirect('account:user_register')
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(
                    user_session['phone_number'],
                    user_session['email'],
                    user_session['fullname'],
                    user_session['password'],
                )
                code_instance.delete()
                messages.success(request, 'user registered', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'code did not match', 'danger')
                return redirect('account:user_verify')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                if self.next is not None:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'user didnt find', 'danger')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')

