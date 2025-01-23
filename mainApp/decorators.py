from django.shortcuts import redirect

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('auth_denied')
    return wrapper_func

def owner_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_owner:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('auth_denied')
    return wrapper_func

def customer_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('auth_denied')
    return wrapper_func