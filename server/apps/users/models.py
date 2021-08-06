from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, RegexValidator


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. From 5 to 20 characters or fewer. Latin letters, digits and @/./+/-/_ only.'),
        validators=[
            UnicodeUsernameValidator(),
            MinLengthValidator(5),
            RegexValidator(r'[^а-яА-ЯёЁ]', code='cyrillic_letters',
                           message=_("Username can only contain letters of the Latin alphabet.")),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
