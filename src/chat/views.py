# i am not using create, update views as i want to write as complex
# class based views as i can. 

import json
from django.views import View
from django.shortcuts import render,redirect
from .models import Room,User
from .forms import AddUserForm, EditUserForm
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView
from django.contrib import messages

# listview only works with a single model. not with multiple models.
class Admin(LoginRequiredMixin):
    def get(self,request,*args,**kwargs):

        rooms=Room.objects.all()
        users=User.objects.filter(is_staff=True)

        return render(request,'chat/admin.html',{'rooms':rooms,'users':users})



class Room(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        room = Room.objects.get(uuid=uuid)

        if room.status == Room.WAITING:
            room.status = Room.ACTIVE
            room.agent = request.user
            room.save()

        return render(request, 'chat/room.html',{'room':room})
    
    def post(self,request,*args,**kwargs):
        
        name = request.POST.get('name','')
        url = request.POST.get('url','')

        uuid = kwargs.get('uuid')

        Room.objects.create(uuid=uuid,client=name,url=url)

        return JsonResponse({'message':'room created'})
    
class User(LoginRequiredMixin,View):
    # not using the permission required mixin on the whole class 
    # becasue the mixin is required for the 
    def post(self,request,*args,**kwargs):
        status = kwargs.get('status')
        if status == 'a':
            if request.user.has_perm('user.add_user'):

                form = AddUserForm(request.POST)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.is_staff=True
                    user.set_password(request.POST.get('password'))
                    user.save()

                    if user.role == User.MANAGER:
                        group = Group.objects.get(name='Managers')
                        group.user_set.add(user)

                    messages.success(request,'The user was added!')

                    # subject to change
                    return redirect('/chat-admin/')

                else:
                    form = AddUserForm()

                return render(request,'chat/add_user.html',{
                    'form':form 
                }) 
            else:
                messages.error(request, 'You dont have access to add users')

                # subject to change.
                return redirect('/chat-admin/')
        
        else:
            if request.user.has_perm('user.edit_user'):
                
                uuid = kwargs.get('uuid')
                user= User.objects.get(pk=uuid)

                form = EditUserForm(request.POST,instance=user)

                if form.is_valid():
                    form.save()

                    messages.success(request,'The changes was saved !')

                    return redirect('/chat-admin/') 
                else:
                    form = EditUserForm(instance=user)

                return render(request,'chat/edit_user.html',{
                    'user':user,'form':form
                })               
            else:
                messages.error(request,'You dont have access to edit users.')

                return redirect('/chat-admin/')
        
    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        user = User.objects.get(pk=uuid)
        rooms = user.rooms.all()

        return render(request,'chat/user_detail.html',{'user':user,'rooms':rooms})

class Delete(LoginRequiredMixin,PermissionRequiredMixin,View):
    
    permission_required='room.delete_room'

    def post(self,request,*args,**kwargs):
        
        uuid = kwargs.get('uuid')

        room = Room.objects.get(uuid=uuid)
        room.delete()

        messages.success(request,'The room was deleted!')

        return redirect('/chat-admin/')

