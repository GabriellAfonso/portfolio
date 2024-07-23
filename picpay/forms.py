from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import re
from validate_docbr import CPF, CNPJ


class RegisterForm(UserCreationForm):
    from django.conf import settings
    settings.AUTH_PASSWORD_VALIDATORS = []

    username = forms.CharField(
        required=False,
        min_length=3,
        max_length=50,
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'Nome de usuário muito curto.',
            'max_length': 'Nome de usuário muito longo.',
        }
    )

    complete_name = forms.CharField(
        required=True,
        min_length=4,
        max_length=50,
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'Nome de usuário muito curto.',
            'max_length': 'Nome de usuário muito longo.',
        }
    )

    email = forms.EmailField(
        required=True,
        max_length=100,
        error_messages={
            'invalid': 'Utilize um e-mail válido',
        }
    )

    document = forms.CharField(
        required=True,
        max_length=100,
        error_messages={
            'required': 'Este campo é obrigatório.',
        }
    )

    sex = forms.ChoiceField(
        required=True,
        choices=[('M', 'Masculino'), ('F', 'Feminino')],
        error_messages={
            'required': 'Este campo é obrigatório.',
        }
    )

    type = forms.ChoiceField(
        required=False,
        choices=[('personal', 'Personal'), ('merchant', 'Merchant')],
        error_messages={
            'required': 'Este campo é obrigatório.',
        }
    )

    balance = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        error_messages={}
    )

    password1 = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        error_messages={
            'required': 'Este campo é obrigatório.',
        },
    )
    password2 = forms.CharField(
        required=False,
        label='Password',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        error_messages={
            'required': 'Este campo é obrigatório.',
        },
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'document', 'sex', 'type', 'balance')

    def clean_complete_name(self):
        name = self.cleaned_data.get('complete_name')
        if not re.match("^[A-Za-zÀ-ÿ ]+$", name):
            raise forms.ValidationError('O nome deve conter apenas letras.')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    forms.ValidationError(
                        'Este e-mail já esta sendo ultilizado.', code='invalid')
                )
        return email

    def clean_document(self):
        document = self.cleaned_data.get('document')
        digits_only = re.sub(r'\D', '', document)

        if len(digits_only) not in (11, 14):
            raise forms.ValidationError(
                'CPF/CNPJ inválido.')

        document_type = self.cpf_or_cpnj(digits_only)

        if document_type == 'cpf':
            document = self.cpf_validator(digits_only)

        if document_type == 'cnpj':
            document = self.cnpj_validator(digits_only)

        return document

    def cpf_or_cpnj(self, document):
        if len(document) == 11:
            return 'cpf'
        return 'cnpj'

    def cpf_validator(self, document):
        cpf = CPF()
        doc = cpf.mask(document)
        if not cpf.validate(doc):
            raise forms.ValidationError('CPF inválido.')
        if Profile.objects.filter(document=doc).exists():
            raise forms.ValidationError('CPF já cadastrado.')

        return doc

    def cnpj_validator(self, document):
        cnpj = CNPJ()
        doc = cnpj.mask(document)
        if not cnpj.validate(doc):
            raise forms.ValidationError('CNPJ inválido.')
        if Profile.objects.filter(document=doc).exists():
            raise forms.ValidationError('CNPJ já cadastrado.')

        return doc

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError(
                'A senha deve ter no mínimo 6 caracteres.'
            )
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
            profile = Profile(
                user=user,
                document=self.cleaned_data['document'],
                sex=self.cleaned_data['sex'],
            )
            profile.save()
        return user
