from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

# 회원가입 폼 (닉네임 포함)
class SignupForm(UserCreationForm):
    nickname = forms.CharField(max_length=30, label='닉네임')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nickname']

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("이미 사용 중인 닉네임입니다.")
        return nickname

    def save(self, commit=True):
        user = super().save(commit)
        nickname = self.cleaned_data['nickname']
        # Profile 연결 후 닉네임 저장
        Profile.objects.update_or_create(user=user, defaults={'nickname': nickname})
        return user


# 사용자 정보 수정 폼 (username, email)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# 프로필 정보 수정 폼 (nickname)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname']

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        # 현재 로그인한 사용자의 프로필은 제외하고 중복 닉네임이 있는지 검사
        if Profile.objects.filter(nickname=nickname).exclude(user=self.instance.user).exists():
            raise forms.ValidationError("이미 사용 중인 닉네임입니다.")
        return nickname


# ✅ 로그인 폼 커스터마이징 (username 라벨 변경)
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
