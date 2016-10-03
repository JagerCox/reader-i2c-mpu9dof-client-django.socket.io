from django.shortcuts import render
from django.views.generic.base import View


class HomeView(View):

    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
