import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from app_API.Friends.viewsFriend import getResourceFriend
from app_API.Groups.Group import *
from app_API.Resources.Resource import Resource
from app_API.Users.User import People


@csrf_exempt
def createGroup(request):
    if request.method == "POST":
        created = json.loads(request.body)
        idLeader = created["idLeader"]
        name_group = created["name_group"]
        leader = People.objects.get(id=idLeader)
        group = Group.objects.create(name=name_group)
        group.leader.add(leader)
        group.save()
    return JsonResponse({"Message": f"{leader.first_name} created this group {group.name}"})


@csrf_exempt
def groupRequest(request):
    if request.method == "POST":
        req = json.loads(request.body)
        idPeople = req["idPeople"]
        id_group = req["id_group"]
        if Group.objects.filter(id=id_group).exists():
            sender = People.objects.get(id=idPeople)
            receiver = Group.objects.get(id=id_group)
            model = RequestGroup.objects.create(sender=sender, receiverGroup=receiver)
            model.save()
            message = {"Message": f"Your request has sending successful to {receiver.name}"}
        else:
            message = {"Message": "This group not found"}
        return JsonResponse(message)


@csrf_exempt
def delete_requestGroup(request):
    if request.method == "POST":
        delete = json.loads(request.body)
        id_leader = delete["id_leader"]
        id_request = delete["id_request"]
        id_group = delete["id_group"]
        if Group.objects.filter(id=id_group).exists():
            req_user = People.objects.get(id=id_request)
            if RequestGroup.objects.filter(sender=req_user).exists():
                leaderUser = People.objects.get(id=id_leader)
                recipient = Group.objects.get(id=id_group, leader=leaderUser)
                model = RequestGroup.objects.get(sender=req_user, receiverGroup=recipient)
                model.delete()
                my_data = {"Message": f"The request friend is deleting by leader {recipient.leader}"}
            else:
                my_data = {"Message": "This user not found"}
        else:
            my_data = {"Message": "This group not found"}

    return JsonResponse(my_data)


@csrf_exempt
def add_or_remove_member(request):
    if request.method == "POST":
        add_or_remove = json.loads(request.body)
        idLeader = add_or_remove["idLeader"]
        id_request = add_or_remove["id_request"]
        id_group = add_or_remove["id_group"]
        operation = add_or_remove["operation"]
        if Group.objects.filter(id=id_group).exists():
            if People.objects.filter(id=id_request).exists():
                my = People.objects.get(id=idLeader)
                group = Group.objects.get(id=id_group, leader=my)
                people = People.objects.get(id=id_request)
                if operation == 'add':
                    fq = RequestGroup.objects.get(sender=people, receiverGroup=group)
                    group.members.add(people)
                    fq.delete()
                    my_data = {"Message": f"Hello our new member {people}"}
                elif operation == 'remove':
                    group.members.remove(people)
                    group.leader.remove(people)
                    my_data = {"Message": f"Sorry {people} you cannot join our group"}
        return JsonResponse(my_data)


@csrf_exempt
def createResource(request):
    if request.method == "POST":
        resources = json.loads(request.body)
        name = resources["name"]
        year = resources["year"]
        color = resources["color"]
        pantone_value = resources["pantone_value"]
        url = resources["url"]
        text = resources["text"]
        id_user = resources["id_user"]
        groupID = resources["groupID"]
        if Group.objects.filter(id=groupID).exists():
            people = People.objects.get(id=id_user)
            group = Group.objects.get(id=groupID)
            if Membership.objects.filter(people=people, group=group):
                group_res = Resource(name=name, year=year, color=color, pantone_value=pantone_value, url=url, text=text
                                     , id_user=id_user, group=group)
                group_res.save()
                my_resource = {"data": group_res.res(), "support": group_res.supports()}
            else:
                my_resource = {"Message": " This user is not a member in this group"}
        else:
            my_resource = {"Message ": " This group not found"}

    return JsonResponse(my_resource)


@csrf_exempt
def getResourceMembers(request):
    if request.method == "POST":
        res = json.loads(request.body)
        id_sender = res["id_sender"]
        id_group = res["id_group"]
        people = People.objects.get(id=id_sender)
        group = Group.objects.get(id=id_group)
        if Membership.objects.filter(people=people, group=group).exists():
            if Resource.objects.filter(group=group).exists():
                message = list(
                    Resource.objects.filter(group=group).values('id_user', 'name', 'year', 'color', 'pantone_value'))
                support = list(Resource.objects.filter(group=group).values('url', 'text'))
                mydata = {"data": message, "support": support}
            else:
                mydata = {"Message ": " In this group , we dont have any resources!!!"}
        else:
            mydata = {"Message": f"You are not member in this group {group.name}"}
        return JsonResponse(mydata)


@csrf_exempt
def getLeaderToMember(request):
    if request.method == "POST":
        res = json.loads(request.body)
        idLeader = res["idLeader"]
        id_member = res["id_member"]
        id_group = res["id_group"]
        leader = People.objects.get(id=idLeader)
        people = People.objects.get(id=id_member)
        group = Group.objects.get(id=id_group)
        if Group.objects.filter(id=id_group, leader=leader).exists():
            if Membership.objects.filter(people=people, group=group).exists():
                group.leader.add(people)
                message = {"Message": f" Hello our new Leader {people.first_name}"}
            else:
                message = {"Message": "This user is not a member in this group!!!"}
        else:
            message = {"Message": "This group not exists!!!"}
        return JsonResponse(message)


@csrf_exempt
def leftLeader(request):
    if request.method == "POST":
        res = json.loads(request.body)
        idLeader = res["idLeader"]
        id_member = res["id_member"]
        id_group = res["id_group"]
        leader = People.objects.get(id=idLeader)
        people = People.objects.get(id=id_member)
        group = Group.objects.get(id=id_group)
        if Group.objects.filter(id=id_group, leader=leader).exists():
            if Group.objects.filter(id=id_group, leader=people).exists():
                group.leader.remove(leader)
                group.save()
                message = {
                    "Message": f"The leader {leader.first_name} left,and the second leader is {people.first_name}"}
            else:
                group.leader.add(people)
                group.leader.remove(leader)
                group.save()
                message = {"Message": f"The leader {leader.first_name} left,and the new leader is {people.first_name}"}
        else:
            message = {"Message": " This group not found "}
        return JsonResponse(message)
