from .decorators import *
    
class LoginRequired:

    login_url = '/useraccountmanagement/login/'
    
    def dispatch(self, request, *args, **kwargs):
        dec = login_required(login_url=self.get_login_url())
        return dec(super().dispatch)(request, *args, **kwargs)

    def get_login_url(self):
        return self.login_url

class PrivilegedRequired:

    login_url = '/useraccountmanagement/login/'

    def dispatch(self, request, *args, **kwargs):
        dec = privileged_required(login_url=self.get_login_url())
        return dec(super().dispatch)(request, *args, **kwargs)

    def get_login_url(self):
        return self.login_url

class UnprivilegedRequired:

    login_url = '/useraccountmanagement/login/'

    def dispatch(self, request, *args, **kwargs):
        dec = unprivileged_required(login_url=self.get_login_url())
        return dec(super().dispatch)(request, *args, **kwargs)

    def get_login_url(self):
        return self.login_url

class CustomerRequired:

    login_url = '/useraccountmanagement/login/'

    def dispatch(self, request, *args, **kwargs):
        dec = customer_required(login_url=self.get_login_url())
        return dec(super().dispatch)(request, *args, **kwargs)

    def get_login_url(self):
        return self.login_url

class DriverRequired:

    login_url = '/useraccountmanagement/login/'

    def dispatch(self, request, *args, **kwargs):
        dec = driver_required(login_url=self.get_login_url())
        return dec(super().dispatch)(request, *args, **kwargs)

    def get_login_url(self):
        return self.login_url
