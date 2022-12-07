import json

from app_API.Friends.Friend import Friend
from app_API.Resources.Resource import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app_API.Users.User import People


@csrf_exempt
def resource(request):
    if request.method == "POST":
        resources = json.loads(request.body)
        name = resources["name"]
        year = resources["year"]
        color = resources["color"]
        pantone_value = resources["pantone_value"]
        url = resources["url"]
        text = resources["text"]
        id_user = resources["id_user"]

        user_res = Resource(name=name, year=year, color=color, pantone_value=pantone_value, url=url, text=text
                            , id_user=id_user)
        user_res.save()
        my_resource = {"data": user_res.res(), "support": user_res.supports()}

    return JsonResponse(my_resource)


@csrf_exempt
def listunknown(request):
    if request.method == "POST":
        data = list(Resource.objects.all().values("id", "name", "year", "color", "pantone_value"))
        support = list(Resource.objects.all().values("url", "text"))
        my_resource = {"data": data, "support": support}
    return JsonResponse(my_resource)


@csrf_exempt
def unknownID(request, ID):
    if request.method == "POST":
        if Resource.objects.filter(id=ID).exists():
            getId = Resource.objects.get(id=ID)
            message = {"data": getId.res(), "support": getId.supports()}
        else:
            message = {}
    return JsonResponse(message)


@csrf_exempt
def sendResource(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_user = data["id_user"]
        if Resource.objects.filter(id_user=id_user).exists():
            message = list(
                Resource.objects.filter(id_user=id_user).values('id_user', 'name', 'year', 'color', 'pantone_value'))
            support = list(Resource.objects.filter(id_user=id_user).values('url', 'text'))
            mydata = {"data": message, "support": support}
        else:
            mydata = {}
        return JsonResponse(mydata)


@csrf_exempt
def add_like(request):
    if request.method == "POST":
        like = json.loads(request.body)
        my_id = like["my_id"]
        id_request = like["id_request"]
        id_resource = like["id_resource"]
        if Friend.objects.filter(id=id_request).exists():
            my = People.objects.get(id=my_id)
            res = Resource.objects.get(id=id_resource)
            if Like.objects.filter(user=my, resource=res).exists():
                createLike = Like.objects.get(user=my, resource=res)
                like_resource = createLike.likes - 1
                createLike.likes = like_resource
                createLike.delete()
                likePost = res.likes - 1
                res.likes = likePost
                res.save()
                message = {"Message": "You already like this post"}
            else:
                createLike = Like.objects.create(user=my, resource=res)
                like_resource = createLike.likes + 1
                createLike.likes = like_resource
                createLike.save()
                likePost = res.likes + 1
                res.likes = likePost
                res.save()
                message = {"Message": "Thanks you for like"}
        else:
            message = {"Message": f"You aren't friends with {id_request.first_name}"}
        return JsonResponse(message)


@csrf_exempt
def add_comment(request):
    if request.method == "POST":
        comment = json.loads(request.body)
        my_id = comment["my_id"]
        id_request = comment["id_request"]
        id_resource = comment["id_resource"]
        write_comment = comment["write_comment"]
        id_comment = comment["id_comment"]
        if Friend.objects.filter(id=id_request).exists():
            my = People.objects.get(id=my_id)
            res = Resource.objects.get(id=id_resource)
            createComment = Comment.objects.create(id=id_comment, user=my, resource=res)
            comment_resource = createComment.comments + write_comment
            createComment.comments = comment_resource
            createComment.save()
            commentPost = res.comments + 1
            res.comments = commentPost
            res.save()
            message = {"Message": f"Thanks you for comment {write_comment}"}
        else:
            message = {"Message": f"You aren't friends with {id_request.first_name}"}
        return JsonResponse(message)


@csrf_exempt
def delete_comment(request):
    if request.method == "POST":
        comment = json.loads(request.body)
        id_resource = comment["id_resource"]
        id_comment = comment["id_comment"]
        if Comment.objects.filter(id=id_comment).exists():
            res = Resource.objects.get(id=id_resource)
            com = Comment.objects.get(id=id_comment)
            com.delete()
            countComment = res.comments - 1
            res.comments = countComment
            res.save()
            message = {"Message": "You delete your comment"}
        else:
            message = {"Message": "No comment for you"}
    return JsonResponse(message)
