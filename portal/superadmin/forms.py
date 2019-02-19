from django import forms


class UserForm(forms.Form):
    fullname = forms.CharField()

    username = forms.CharField()

    email = forms.CharField()

    # phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_messages={"invalid": "số điện thoại không hợp lệ"})

    password = forms.CharField()

    password2 = forms.CharField()

    # check password
    def clean_password2(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password2 = self.cleaned_data['password2']
            if password == password2 and password:
                return password2
            else:
                raise forms.ValidationError("Re-password doesn't match!")
        raise forms.ValidationError("Password is invalid!")


    # check xem user name đã tồn tại hay chưa
    def clean_username(self):
        username =  self.cleaned_data['username']
        if get_user(username) is not None:
            raise forms.ValidationError("Username was existed!")
        return username

    # check email có đúng định dạng không, đã tồn tại chưa
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_users_email(email) is not None:
            raise forms.ValidationError("Email was registered!")
        try:
            validate_email(email)
        except:
            raise forms.ValidationError("Email is invalid!")
        return email


    # lưu tài khoản User
    def save(self):
        u = MyUser.objects.create_user(fullname=self.cleaned_data['fullname'], username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password'], key=binascii.hexlify(os.urandom(24)).decode("utf-8"))
        return u

class UserResetForm(forms.Form):
    uemail = forms.CharField( )

    # check email xem đã tồn tại chưa, đúng định dạng không
    def clean_uemail(self):
        uemail = self.cleaned_data['uemail']
        try:
            validate_email(uemail)
        except:
            raise forms.ValidationError("Email is invalid")
        if get_users_email(uemail) is None:
            raise forms.ValidationError("Email isn't registered")
        return uemail


# form thay đổi mật khẩu mới khi User bấm vào link xác nhận trong email
class ResetForm(forms.Form):
    pwd1 = forms.CharField(widget=forms.PasswordInput(
        attrs={               
            'class': 'form-control',
        }
    ))

    pwd2 = forms.CharField(widget=forms.PasswordInput(
        attrs={               
            'class': 'form-control',
        }
    ))

    # check mật khẩu 
    def clean(self):
        if 'pwd1' in self.cleaned_data:
            pwd1 = self.cleaned_data['pwd1']
            pwd2 = self.cleaned_data['pwd2']
            if pwd1 == pwd2 and pwd1:
                return pwd1
            else:
                raise forms.ValidationError("Re-password does not match!")
        raise forms.ValidationError("Password is invalid!")


class PaymentForm(forms.Form):

    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)