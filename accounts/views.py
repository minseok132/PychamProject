from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

# ✅ 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # 폼이 유효하지 않으면 다시 렌더링 (닉네임 중복 등)
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

# ✅ 프로필 보기 뷰
@login_required
def profile_view(request):
    # 프로필이 없으면 자동 생성
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'registration/profile.html', {
        'user': request.user,
        'nickname': profile.nickname,
    })

# ✅ 회원 정보 수정 뷰 (닉네임 포함)
@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'registration/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# ✅ 로그인 뷰 (사용자 이름 -> 아이디 라벨 커스텀 폼 사용)
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm


