from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template


def example_page(request):
    context = {"title": "Example"}
    template_name = "hello_world.html"
    template_obj = get_template(template_name)
    rendered_item = template_obj.render(context)
    return HttpResponse(rendered_item)


def redirect_view(request):
    return redirect('/stock/deal/')
