from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message

@login_required
def chat_list(request):
    # 사용자가 참여 중인 모든 채팅방
    rooms = request.user.chatrooms.all().order_by('-created_at')
    return render(request, 'chat/chat_list.html', {'rooms': rooms})

@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)

    # 나와 다른 사용자 간 채팅방을 찾거나 새로 생성
    chat_rooms = ChatRoom.objects.filter(participants=request.user).filter(participants=other_user)
    if chat_rooms.exists():
        room = chat_rooms.first()
    else:
        room = ChatRoom.objects.create()
        room.participants.add(request.user, other_user)

    return redirect('chat:room_detail', room_id=room.id)

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(room=room, sender=request.user, text=text)
            return redirect('chat:room_detail', room_id=room.id)  # 새로고침으로 반영!

    messages = room.messages.order_by('created_at')
    return render(request, 'chat/room_detail.html', {
        'room': room,
        'messages': messages,
    })

