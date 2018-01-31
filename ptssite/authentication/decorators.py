from functools import wraps
from django.http import HttpResponseRedirect

def _pass_test(test, redirect_url):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if test(request):
                return view(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(redirect_url)
        return wrapper
    return decorator

def login_required(view=None, login_url='/useraccountmanagement/login/'):
    decorator = _pass_test(lambda request: request.user.is_authenticated(),
                           login_url)
    if view:
        return decorator(view)
    return decorator

def privileged_required(view=None, login_url='/systemmanagement/login/'):
    decorator = _pass_test(lambda request: request.user.is_authenticated()
                           and not request.user.is_unprivileged(), login_url)
    if view:
        return decorator(view)
    return decorator

def unprivileged_required(view=None, login_url='/useraccountmanagement/login/'):
    decorator = _pass_test(lambda request: request.user.is_authenticated()
                           and request.user.is_unprivileged(), login_url)
    if view:
        return decorator(view)
    return decorator

def driver_required(view=None, login_url='/useraccountmanagement/login/'):
    decorator = _pass_test(lambda request: request.user.is_authenticated()
                           and request.user.is_unprivileged()
                           and request.user.unprivilegeduser.is_driver(),
                           login_url)
    if view:
        return decorator(view)
    return decorator

def customer_required(view=None, login_url='/useraccountmanagement/login/'):
    decorator = _pass_test(lambda request: request.user.is_authenticated()
                           and request.user.is_unprivileged()
                           and request.user.unprivilegeduser.is_customer(), login_url)
    if view:
        return decorator(view)
    return decorator
