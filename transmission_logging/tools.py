import re
import json

def get_headers(request):
    regex = re.compile('^HTTP_')
    return {
        regex.sub('', header): value
        for (header, value) in request.META.items() 
        if header.startswith('HTTP_')
    }

def get_request_content(request):
    request_content = {
        key: value for key, value in request.GET.items()
    }
    if request.method == "POST":
        try:
            request_content = json.loads(request.body)
        except json.JSONDecodeError:
            request_content = {
                key: value for key, value in request.POST.items()
            }
    return request_content