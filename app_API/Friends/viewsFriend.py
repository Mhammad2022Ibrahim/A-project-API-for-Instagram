import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app_API.Friends.Friend import Friend, FriendRequest
from app_API.Resources.Resource import Resource
from app_API.Users.User import People


@csrf_exempt
def sendRequest(request):
    if request.method == "POST":
        friend_req = json.loads(request.body)
        id_sender = friend_req["id_sender"]
        id_request = friend_req["id_request"]

        if People.objects.filter(id=id_request).exists():
            sender = People.objects.get(id=id_sender)
            recipient = People.objects.get(id=id_request)
            model = FriendRequest.objects.get_or_create(sender=sender, receiver=recipient)
            # model.save()
            my_message = {"Message": f"The friend request is sending to {recipient.first_name}"}
        else:
            my_message = {"Message": "This user not found"}

    return JsonResponse(my_message)


@csrf_exempt
def delete_request(request):
    if request.method == "POST":
        delete = json.loads(request.body)
        id_sender = delete["id_sender"]
        id_request = delete["id_request"]
        operation = delete["operation"]
        if People.objects.filter(id=id_request).exists():
            sender = People.objects.get(id=id_sender)
            recipient = People.objects.get(id=id_request)
            if operation == 'Sender_deleting':
                model1 = FriendRequest.objects.get(sender=sender, receiver=recipient)
                model1.delete()
                my_data = {"Message": "I delete the request"}
            elif operation == 'Receiver_deleting':
                model2 = FriendRequest.objects.get(sender=sender, receiver=recipient)
                model2.delete()
                my_data = {"Message": "The request friend is deleting"}

        return JsonResponse(my_data)


@csrf_exempt
def add_or_remove_friend(request):
    if request.method == "POST":
        add_or_remove = json.loads(request.body)
        id1 = add_or_remove["id1"]
        id_request = add_or_remove["id_request"]
        operation = add_or_remove["operation"]
        if People.objects.filter(id=id_request).exists():
            my = People.objects.get(id=id1)
            new_friend = People.objects.get(id=id_request)
            if operation == 'add':
                fq = FriendRequest.objects.get(sender=new_friend, receiver=my)
                Friend.make_friend(my, new_friend)
                Friend.make_friend(new_friend, my)
                fq.delete()
                my_data = {"Message": f"Hello my new friend {new_friend}"}
            elif operation == 'remove':
                Friend.lose_friend(my, new_friend)
                Friend.lose_friend(new_friend, my)
                my_data = {"Message": f"Sorry {new_friend} we cannot are friends"}
        return JsonResponse(my_data)


@csrf_exempt
def getResourceFriend(request):
    if request.method == "POST":
        res = json.loads(request.body)
        id_sender = res["id_sender"]
        id_request = res["id_request"]
        if Friend.objects.filter(id=id_request).exists():
            message = list(
                Resource.objects.filter(id_user=id_request).values('id_user', 'name', 'year', 'color', 'pantone_value'))
            support = list(Resource.objects.filter(id_user=id_request).values('url', 'text'))
            mydata = {"data": message, "support": support}
        else:
            mydata = {"Message": "You are not friend with this account, you cannot access to his resources"}
        return JsonResponse(mydata)
