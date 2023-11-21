from contextvars import Token

import rest_framework_simplejwt.authentication
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Member
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, MemberForm
from rest_framework import viewsets, permissions, views, authentication, status
from .serializers import MemberSerializer, UserSerialized
from django.http import JsonResponse


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListUsers(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialized
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        # user, token = rest_framework_simplejwt.authentication.JWTAuthentication.authenticate(request)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                # 'token' : str(token),
            })
        else:
            return JsonResponse({
                "response": "Wrong password or username"
            })


class MembersView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        members = Member.objects.all()
        data = MemberSerializer(members, many=True).data
        return JsonResponse(data, safe=False)

    def post(self, request):
        # data = {
        #     'firstname': request.data.get('firstname'),
        #     'lastname': request.data.get('lastname'),
        #     'phone': request.data.get('phone'),
        #     'joined_date': request.data.get('joined_date'),
        # }
        # print(data)
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class MemberDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        # member = Member.objects.get(id=id)
        member = Member.objects.filter(id=id).first()
        if member is None :
            return JsonResponse({
                "response": "No member with this id"
            })
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, id):
        # member = Member.objects.get(id=id)
        member = Member.objects.filter(id=id).first()
        if member is None:
            return JsonResponse({
                "response": "No member with this id"
            })
        serializer = MemberSerializer(instance=member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        # try:
        #     member = Member.objects.get(id=id)
        # except Member.DoesNotExist:
        #     return Response(
        #         {"response": "No member with this id"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        member = Member.objects.filter(id=id).first()
        if member is None:
            return JsonResponse({
                "response": "No member with this id"
            })
        member.delete()
        return Response(
            {"response": "Member deleted!"},
            status=status.HTTP_200_OK
        )

@login_required
def members(request):
    if (request.method == 'GET'):

        mymembers = Member.objects.all().values()

        context = {
            'mymembers': mymembers,
            'form': MemberForm()
        }
        return render(request, 'all_members.html', context)
    elif request.method == 'POST':
        if 'save' in request.POST:
            form = MemberForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('members')


@login_required
def details(request, id):
    mymember = Member.objects.get(id=id)

    if (request.method == 'GET'):
        template = loader.get_template('details.html')
        context = {
            'mymember': mymember,
        }
        return HttpResponse(template.render(context, request))
    elif (request.method == 'POST'):
        if 'remove' in request.POST:
            mymember.delete()
        elif 'save' in request.POST:
            mymember.phone = request.POST.get("phone")
            mymember.joined_date = request.POST.get("joined_date")
            mymember.save()
        return redirect('members')


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())


def testing(request):
    mydata = Member.objects.filter(firstname__startswith='L').values()
    template = loader.get_template('template.html')
    context = {
        'mymembers': mydata,
    }
    return HttpResponse(template.render(context, request))


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('members')
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('members')

        messages.error(request, f'Invalid username or password')
        return render(request, 'login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


# def delete_post(request, id):
#     member = get_object_or_404(Member, pk=id)
#     # context = {'post': post}
#     # if request.method == 'GET':
#     #     return render(request, 'blog/post_confirm_delete.html', context)
#     # elif
#     if request.method == 'POST':
#         print("should be running")
#         member.delete()
#         return redirect('members')
#
#
# @login_required
# def edit_post(request, id):
#     post = get_object_or_404(Post, id=id)
#
#     if request.method == 'GET':
#         context = {'form': PostForm(instance=post), 'id': id}
#         return render(request, 'blog/post_form.html', context)
#
#     elif request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, 'The post has been updated successfully.')
#             return redirect('posts')
#         else:
#             messages.error(request, 'Please correct the following errors:')
#             return render(request, 'blog/post_form.html', {'form': form})


@login_required
def add(request):
    if request.method == 'GET':
        context = {'form': MemberForm()}
        return render(request, 'test/add_member.html', context)
    elif request.method == 'POST':
        if 'save' in request.POST:
            form = MemberForm(request.POST)
            if form.is_valid():
                form.save()
                # messages.success(
                #     request, 'The post has been created successfully.')
                return redirect('members')
            else:
                # messages.error(request, 'Please correct the following errors:')
                return render(request, 'test/add_member.html', {'form': form})
        # elif 'cancel' in request.POST:
        #     form = MemberForm(request.POST)
        #     form.
        #     form.empty_permitted = True
        #     return redirect('members')
