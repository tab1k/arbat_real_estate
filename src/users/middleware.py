from django.shortcuts import redirect


class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Проверка: если пользователь суперпользователь, то ему разрешено все
            if request.user.is_superuser:
                return self.get_response(request)

            # Проверяем роль пользователя в зависимости от URL
            if request.path.startswith('/managers/') and request.user.role != 'manager':
                return redirect('users:role_exists')  # Например, URL 'users:role_exists'
            elif request.path.startswith('/realtors/') and request.user.role != 'realtor':
                return redirect('users:role_exists')

        # Если все ок, передаем запрос дальше
        response = self.get_response(request)
        return response
