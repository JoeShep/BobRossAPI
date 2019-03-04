from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from api.models import Customer
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
                    username=req_body['username'],
                    password=req_body['password'],
                    email=req_body['email'],
                    first_name=req_body['first_name'],
                    last_name=req_body['last_name'],
                    )

    new_customer = Customer.objects.create(
                    user = new_user,
                    street_address=req_body['street'],
                    city=req_body['city'],
                    state=req_body['state'],
                    zipcode=req_body['zip'],
                  )

    # Use the REST Framework's token generator on the new user account
    # This is the same as calling a method for loggin in a user after you create their account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token":token.key})
    return HttpResponse(data, content_type='application/json')
