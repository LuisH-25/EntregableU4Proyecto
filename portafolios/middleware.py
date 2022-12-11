from django.http import HttpResponse
from ipware import get_client_ip

BLACK_LISTED_IPS = [
    '127.0.0.1'
]

class ip_is_valid:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        print(ip)
        print(is_routable)

        if ip in BLACK_LISTED_IPS:
            # 403 - Forbidden
            # raise PermissionDenied
            # return defaults.permission_denied(request, '', template_name='403.html')

            # 404 - Not Found
             return HttpResponse('Bad Request', status = 404)
            # return defaults.page_not_found(request, 'ERROR', template_name='404.html')
            #return render(request, 'Custom404.html')

            # 500 - Server Error
            # return defaults.server_error(request, template_name='500.html')

            # 400 - Bad Request
            # return defaults.bad_request(request, '', template_name='400.html')
        else:
            return self.get_response(request)