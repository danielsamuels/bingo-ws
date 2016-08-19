from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import generic

admin.autodiscover()

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r'^$', generic.TemplateView.as_view(template_name='chat.html'))
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)


if settings.DEBUG:
    urlpatterns += [
        url(r"^404/$", generic.TemplateView.as_view(template_name="404.html")),
        url(r"^500/$", generic.TemplateView.as_view(template_name="500.html")),
    ]
