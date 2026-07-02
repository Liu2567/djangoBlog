from django.utils.deprecation import MiddlewareMixin

class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 对 /auth/register 和 /auth/login 路径禁用 CSRF 验证
        if request.path.startswith('/auth/'):
            setattr(request, '_dont_enforce_csrf_checks', True)