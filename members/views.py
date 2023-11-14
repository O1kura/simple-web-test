from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Member
from django.contrib.auth import login,authenticate,logout
from .forms import LoginForm, MemberForm

@login_required
def members(request):
    mymembers = Member.objects.all().values()
    # form = MemberForm(request.POST)
    # if form.is_valid():
    #     form.save()
    template = loader.get_template('all_members.html')

    context = {
        'mymembers': mymembers,
        # 'form':form
    }
    # return HttpResponse(template.render(context,request))
    return render(request, 'all_members.html', context)

@login_required
def details(request, id):
    mymember = Member.objects.get(id=id)

    if (request.method=='GET'):
        template = loader.get_template('details.html')
        context = {
            'mymember': mymember,
        }
        return HttpResponse(template.render(context, request))
    elif(request.method=='POST'):
        if 'remove' in request.POST:
            mymember.delete()
        elif 'save' in request.POST:
            print("sth")
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
            'form':form
        }
        return render(request, 'login.html', context )
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
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(
            #     request, 'The post has been created successfully.')
            return redirect('members')
        else:
            # messages.error(request, 'Please correct the following errors:')
            return render(request, 'test/add_member.html', {'form': form})
