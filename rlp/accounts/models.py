import logging
import re

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.sessions.models import Session
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)

phone_digits_re = re.compile(r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4}).*$')


class Institution(models.Model):
    name = models.CharField(max_length=255)
    banner_image = models.ImageField(upload_to='institutions', blank=True)
    thumbnail_image = models.ImageField(upload_to='institutions', blank=True)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class InstitutionDomain(models.Model):
    institution = models.ForeignKey(Institution)
    domain = models.CharField(max_length=200)

    class Meta:
        unique_together = ['institution', 'domain']

    def __str__(self):
        return self.domain


class UserManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name.lower(), domain_part.lower()])
        return email

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Email and password are required. Other fields are optional.
    """
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    title = models.CharField(max_length=255, blank=True, verbose_name='Title, Department')
    degrees = models.CharField(max_length=20, blank=True, help_text='MD, PhD, etc.')
    bio = models.TextField(blank=True, max_length=3000)
    research_interests = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True, help_text='Enter the full url e.g. https://twitter.com/username')
    orcid = models.CharField(
        verbose_name='ORCID ID',
        max_length=100,
        blank=True,
        help_text='If you do not have an ORCID ID, you can register for one '
                  '<a href="https://orcid.org/register" target="_blank">here</a>')
    photo = models.ImageField(upload_to="profile_photos", blank=True)
    institution = models.ForeignKey(Institution, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return "{0} {1} ({2})".format(self.first_name, self.last_name, self.email)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('profile', args=[self.pk])

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    @property
    def can_access_all_projects(self):
        # If the user belongs to a single 'private' project or is an admin, they can access any project on the site
        return any(self.projectmembership_set.values_list('project__approval_required', flat=True)) or self.is_staff


class UserLogin(models.Model):
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} logged in {}".format(self.user.get_full_name(), self.date_created.strftime("%Y-%m-%d %H:%M:%S %z"))
