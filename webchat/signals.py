from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message


@receiver(post_save, sender=Message)
def delete_oldest_message(sender, instance, **kwargs):
    room = instance.room
    message_count = room.message_set.count()
    max_message_count = 800

    if message_count > max_message_count:
        oldest_message = room.message_set.order_by('timestamp').first()
        oldest_message.delete()
