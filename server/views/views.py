from django.views.generic import TemplateView


class HomePageView(TemplateView):
    '''Serve a static index.html file for the root directory of backend'''
    template_name = "index.html"
