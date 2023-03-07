from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from root.breadcrumb import BreadCrumb
from .forms import RegisterForm, UserEditFormView, ProfileEditFormView, UserEditForm, ProfileEditForm, UserProfileInfo, \
    ResidentialInfoForm, ChangeProfilePicForm

def sign_up_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password'])
            messages.success(request, "Account created successfully!")
            new_user.save()
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user}
            )
    else:
        form = RegisterForm()
    return render(
        request,
        'accounts/register.html',
        {"form": form, 'title': 'Sign Up'}
    )


@login_required
@require_http_methods(["GET"])
def view(request):
    user_form = UserEditFormView(instance=request.user)
    profile_form = ProfileEditFormView(
        instance=request.user.userprofile
    )
    return render(
        request,
        'accounts/profile.html',
        {'user_form': user_form,
         'profile_form': profile_form,
         'status': 'disabled'
         }
    )


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.userprofile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('view_profile')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.userprofile
        )
    return render(
        request,
        'accounts/profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'status': 'enabled',
            'title': 'Edit Profile'
         }
    )

@login_required
def profile(request):
    bread_crumb = [
        BreadCrumb("Home", "/"),
        BreadCrumb("Profile", reverse('profile'), True),
    ]
    user_form = UserEditForm(instance=request.user)
    profile_form = UserProfileInfo(instance=request.user.userprofile)
    residential_info_form = ResidentialInfoForm(instance=request.user.residentialinfo)
    image_form = ChangeProfilePicForm(instance=request.user.userprofile)

    if request.method == 'POST':
        residential_info_form = ResidentialInfoForm(data=request.POST, instance=request.user.residentialinfo)
        profile_form = UserProfileInfo(data=request.POST, instance=request.user.userprofile)
        user_form = UserEditForm(instance=request.user, data=request.POST)
        image_form = ChangeProfilePicForm(data=request.POST, files=request.FILES)

        if residential_info_form.is_valid() and profile_form.is_valid() and user_form.is_valid() and image_form.is_valid():
            residential_info_form.save()
            _profile = profile_form.save(commit=False)
            _profile.image = image_form.cleaned_data['image']
            _profile.save()
            user_form.save()
            # image_form.save()
            messages.success(request, "Profile updated successfully")
    return render(
        request, 
        'accounts/my_profile.html',
        {
            'residential_info_form': residential_info_form, 
            'user_form': user_form,
            'profile_form': profile_form, 
            'bread_crumb': bread_crumb, 
            'image_form': image_form,
        }
    )


