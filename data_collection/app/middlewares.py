from django.shortcuts import redirect

def firstmiddleware(get_response):
    def middleware(request):
        returnUrl = ''
        if not request.session.get('user'):
            return redirect('login')
        response = get_response(request)
        return response
    return middleware


def secondmiddleware(get_response):
    def middleware(request, project_id=None):
        returnUrl = ''
        print(request.META['PATH_INFO'])
        if not request.session.get('user'):
            return redirect('login')
        response = get_response(request, project_id=project_id)
        return response
    return middleware
