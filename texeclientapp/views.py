from django.shortcuts import render
from django.http import HttpResponse



def index(request):

#     context = {
#         'page_title': 'My Django Project',
#         'header_text': 'Welcome to Django!',
#         'footer_text': '© 2023 My Django Project',
    # }
    # return render(request, 'index.html', context)
    return HttpResponse("hello")