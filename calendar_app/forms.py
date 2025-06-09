# calendar_app/forms.py

from django import forms
from .models import CafeteriaMenu, MenuPhoto

class CafeteriaMenuForm(forms.ModelForm):
    """
    날짜별 학식 메뉴 텍스트를 입력/수정하는 폼
    """
    class Meta:
        model = CafeteriaMenu
        fields = ['date', 'menu_text']
        widgets = {
            # 달력에서 클릭된 날짜를 숨겨진 필드로 전달
            'date': forms.HiddenInput(),
            # 메뉴 입력 영역 크기 커스터마이징
            'menu_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class MenuPhotoForm(forms.ModelForm):
    """
    학식 메뉴 사진을 업로드하는 폼
    """
    class Meta:
        model = MenuPhoto
        fields = ['image']
        widgets = {
            # 단일 파일 업로드 (multiple=False 기본값)
            'image': forms.ClearableFileInput(),
        }
