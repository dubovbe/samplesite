from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from bboard.forms import BbForm, RegisterUserForm
from bboard.models import Bb, Rubric, AdvUser, ChangeUserInfoForm
from bboard.serializers import RubricSerializer, BbSerializer
from bboard.utilities import signer


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


def other_page(request, page):
    temp_page = 'bboard/' + page + '.html'
    try:
        get_template(temp_page)
    except TemplateDoesNotExist:
        raise Http404
    return render(request, temp_page)
    # return HttpResponse(template.render(request=request))


class BbCreateView(CreateView):
    """
    Создание нового объявления
    """
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbLoginView(LoginView):
    template_name = 'bboard/login.html'
    success_url = reverse_lazy('profile')


@login_required
def profile(request):
    """
    Профиль пользователя
    """
    return render(request, 'bboard/profile.html')


class BbLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'bboard/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """
    Правка личных данных пользователя
    """
    model = AdvUser
    template_name = 'bboard/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChangeUserPasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'bboard/change_password.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль пользователя успешно изменен'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'bboard/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'bboard/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'bboard/delete_user.html'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# class APIRubrics(APIView):
#     def get(self, request):
#         rubrics = Rubric.objects.all()
#         serializer = RubricSerializer(rubrics, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = RubricSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIRubricViewSet(ModelViewSet):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


class APIBbViewSet(ModelViewSet):
    queryset = Bb.objects.all()
    serializer_class = BbSerializer


class APIRubrics(generics.ListCreateAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


class APIRubricDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer


class APIBbs(generics.ListCreateAPIView):
    queryset = Bb.objects.all()
    serializer_class = BbSerializer


class APIBbDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bb.objects.all()
    serializer_class = BbSerializer


def user_register_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'bboard/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'bboard/user_is_activated.html'
    else:
        template = 'bboard/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


@api_view(['GET'])
def api_bbs_by_rubric(request, rubric_id):
    if request.method == 'GET':
        bbs = Bb.objects.filter(rubric_id=rubric_id)
        serializer = BbSerializer(bbs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_bb_detail(request, pk):
    if request.method == 'GET':
        bb = Bb.objects.get(pk=pk)
        serializer = BbSerializer(bb)
        return Response(serializer.data)
