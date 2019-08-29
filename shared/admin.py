from django.contrib import admin
from django.conf.urls import url


class CustomURLModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        additional_urls = []

        for custom_url in self.custom_urls:
            view = custom_url['view'].as_view()
            custom_url['view'] = self.admin_site.admin_view(view)
            additional_urls.append(url(**custom_url))

        return additional_urls + urls
