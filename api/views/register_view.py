from django.http import HttpResponse
from django.contrib.auth.models import User, Group
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

    # Commit the user to the database by saving it
    new_user.save()

    # Use the REST Framework's token generator on the new user account
    # This is the same as calling a method for loggin in a user after you create their account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    # This doesn't look like how the docs say you should do it.
    # Authorization: Token 93138ba960dfb4ef2eef6b907718ae04400f606a
    # Isn't this sending the data back in the body of the response instead of the header?
    data = json.dumps({"token":token.key})
    return HttpResponse(data, content_type='application/json')
