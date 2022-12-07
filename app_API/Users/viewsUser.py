import json
from app_API.Resources.Resource import Resource
from app_API.Users.User import People
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token


# Create your views here.
@csrf_exempt
def createUsers(request):
    if request.method == "POST":
        message = json.loads(request.body)
        name = message["name"]
        job = message["job"]
        create_user = People(first_name=name, job=job)
        create_user.save()
        my_message = create_user.create()

    return JsonResponse(my_message)


@csrf_exempt
def listUsers(request):
    if request.method == "POST":
        data = list(People.objects.all().values("id", "email", "first_name", "last_name", "avatar"))
        support = list(People.objects.all().values("url", "text"))
        my_message = {"data": data, "support": support}
        return JsonResponse(my_message)


@csrf_exempt
def updateUSer(request):
    if request.method == "POST":
        message = json.loads(request.body)
        name = message["name"]
        job = message["job"]
        update_user = People(first_name=name, job=job)
        update_user.save()
        my_message = update_user.update()
        return JsonResponse(my_message)


@csrf_exempt
def deleteUser(request):
    if request.method == "POST":
        People.objects.all().delete()
        my_message = {}
        return JsonResponse(my_message)


@csrf_exempt
def userID(request, ID):
    if request.method == "POST":
        if People.objects.filter(id=ID).exists():
            getId = People.objects.get(id=ID)
            my_message = {"data": getId.datas(), "support": getId.supports()}
        else:
            my_message = {}
        return JsonResponse(my_message)


@csrf_exempt
# Create your views here.
def register(request):
    if request.method == 'POST':
        message = json.loads(request.body)
        email = message["email"]
        first_name = message["first_name"]
        last_name = message["last_name"]
        avatar = message["avatar"]
        url = message["url"]
        text = message["text"]
        username = message["username"]
        password = message["password"]

        if People.objects.filter(email=email).exists():
            my_message = {"message": "Cannot register!!This email is already register."}

        else:
            user1 = User.objects.create_user(username=username, password=password, email=email)
            token, created = Token.objects.get_or_create(user=user1)
            user = People(user=user1,
                          email=email,
                          first_name=first_name,
                          last_name=last_name,
                          avatar=avatar,
                          url=url,
                          text=text,
                          token=token.key)

            user.save()
            my_message = {'id': user.id, 'token': user.token}

        return JsonResponse(my_message)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        resource = json.loads(request.body)
        idUser = resource["id"]
        token = resource["token"]
        if People.objects.filter(token=token).exists():
            if Resource.objects.filter(id_user=idUser).exists():
                my_resource = list(
                    Resource.objects.filter(id_user=idUser).values('id_user', 'name', 'year', 'color', 'pantone_value'))
                support = list(Resource.objects.filter(id_user=idUser).values('url', 'text'))

                resources = {"data": my_resource, "support": support}
            else:
                resources = {}
        else:
            resources = {"Error": "Invalid token!!"}
    return JsonResponse(resources)


@csrf_exempt
def sendPeople(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_user = data["id_user"]
        if People.objects.filter(id=id_user).exists():
            message = People.objects.get(id=id_user)
            mydata = {"data": message.datas(), "support": message.supports()}
        else:
            mydata = {}
        return JsonResponse(mydata)
