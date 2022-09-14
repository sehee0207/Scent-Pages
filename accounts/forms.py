from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
            return email
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", )
        
class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password(self):
        # 기존 암호
        old_password = self.cleaned_data.get('password2')
        
        # 새로운 암호
        new_password = super().clean_new_password()
        
        # 만약 기존 암호와 새로운 암호가 같다면
        if old_password == new_password:
            raise forms.ValidationError("변경할 암호가 기존 암호와 달라야 합니다")
        
        return new_password