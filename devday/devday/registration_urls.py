"""
URLconf for django_registration and activation, using django-django_registration's
HMAC activation workflow.

"""

from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django_registration.backends.activation import views

urlpatterns = [
    url(r'^activate/complete/$',
        TemplateView.as_view(
            template_name='django_registration/activation_complete.html'
        ),
        name='registration_activation_complete'),
    # The activation key can make use of any character from the
    # URL-safe base64 alphabet, plus the colon as a separator.
    url(r'^activate/(?P<activation_key>[-:\w]+)/$',
        views.ActivationView.as_view(),
        name='registration_activate'),
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='django_registration/registration_complete.html'
        ),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(
            template_name='django_registration/registration_closed.html'
        ),
        name='registration_disallowed'),
    url(r'', include('devday.auth_urls')),
]
