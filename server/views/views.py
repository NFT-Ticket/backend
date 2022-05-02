from django.views.generic import TemplateView


class HomePageView(TemplateView):
    '''Serve a static index.html file for the root directory of backend'''
    template_name = "index.html"


class VerifiedView(TemplateView):
    '''Serve a static verified ticket html for demo purposes'''
    template_name = "verified.html"


class NotVerifiedView(TemplateView):
    '''Serve a not verified ticket html for demo purposes'''
    template_name = "not_verified.html"
