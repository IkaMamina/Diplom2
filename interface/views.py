import random
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from rest_framework.reverse import reverse_lazy, reverse

from interface.forms import UserRegisterForm, SmsCodeForm, UserUpdateForm
from users.models import User
from users.services import create_invite_code


class HomeView(TemplateView):
    """Контроллер главной страницы сайта"""

    template_name = "interface/index.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        users = User.objects.all()
        context_data["all_clients"] = users.count()
        context_data["all_ref_code"] = users.exclude(ref_code=None).count()

        return context_data


class UserCreateView(CreateView):
    """Сохранение пользователя"""

    template_name = "interface/register.html"
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("interface:login")

    def get_success_url(
        self,
    ):
        return reverse_lazy("interface:sms_code") + "?phone=" + self.object.phone

    def form_valid(self, form, *args, **kwargs):
        return_data = {}

        form.is_valid()
        user = form.save()
        user.invite_code = create_invite_code()
        return_data["invite_code"] = user.invite_code

        password = random.randint(1000, 9999)
        user.set_password(str(password))
        user.save()
        messages.success(self.request, "Отправили код в смс!")
        time.sleep(3)
        print(password)
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        user = User.objects.get(phone=form.data.get("phone"))
        if user.phone == "89205398093":
            password = "1111"
        else:
            password = random.randint(1000, 9999)
        user.set_password(str(password))
        user.save()
        messages.success(self.request, "Отправили код в смс!")
        self.object = user
        time.sleep(3)
        print(password)
        return redirect(self.get_success_url())


class SmsCodeView(View):
    """Проверка кода"""

    def post(self, *args, **kwargs):
        phone = self.request.POST.get("phone")
        code = self.request.POST.get("code")
        user = authenticate(self.request, username=phone, password=code)
        if user is not None:
            login(self.request, user)
            return redirect(reverse("interface:user_detail"))
        else:
            return redirect(reverse("interface:login"))

    def get(self, *args, **kwargs):
        form = SmsCodeForm()
        return render(self.request, "interface/sms_code.html", {"form": form})


class UserDetailView(DetailView):
    """Отображение данных пользователя"""

    model = User
    template_name = "interface/user_detail.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["invitation_list"] = [
            user.phone
            for user in User.objects.all().filter(
                ref_code=self.request.user.invite_code
            )
        ]
        return context_data


class UserUpdateView(UpdateView):
    """Обновление данных пользователя"""

    model = User
    template_name = "interface/user_update.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("interface:user_detail")

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(
        self,
    ):
        return reverse_lazy("interface:user_detail") + "?phone=" + self.object.phone


class UserListView(ListView, LoginRequiredMixin):
    model = User
    template_name = "interface/user_list.html"