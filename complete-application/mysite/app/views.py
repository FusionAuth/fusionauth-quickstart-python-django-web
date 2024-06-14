from json import loads
from math import ceil
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

def app(request):
    if not request.user.is_authenticated:
        return render(request, template_name='home.html')
    return redirect('account')

def account(request):
    if not request.user.is_authenticated:
        return redirect('oidc_authentication_init')
    return render(request, 'account.html', {'email': request.user.email})

# https://mozilla-django-oidc.readthedocs.io/en/stable/installation.html
# When a user logs out, by default, mozilla-django-oidc will end the current Django session. 
# However, the user may still have an active session with the OpenID Connect provider, in which case, 
# the user would likely not be prompted to log back in.

# Some OpenID Connect providers support a custom (not part of OIDC spec) mechanism to end 
# the provider’s session. We can build a function for OIDC_OP_LOGOUT_URL_METHOD that will r
# edirect the user to the provider after mozilla-django-oidc ends the Django session.

# def provider_logout(request):
#     # See your provider's documentation for details on if and how this is
#     # supported
#     redirect_url = 'https://myprovider.com/logout'
#     return redirect_url

def change(request):
    if not request.user.is_authenticated:
        return redirect('oidc_authentication_init')
    change = { "error": None }
    if request.method == 'POST':
        dollar_amt_param = request.POST.get("amount")
        try:
            if dollar_amt_param:
                dollar_amt = float(dollar_amt_param)
                nickels = int(dollar_amt / 0.05)
                pennies = ceil((dollar_amt - (0.05 * nickels)) / 0.01)
                change["total"] = "{:,.2f}".format(dollar_amt)
                change["nickels"] = "{:,d}".format(nickels)
                change["pennies"] = "{:,d}".format(pennies)
        except ValueError:
            change["error"] = "Please enter a dollar amount"
    return render(
        request,
        'change.html',
        {
            'email': request.user.email,
            'change': change
        }
    )
