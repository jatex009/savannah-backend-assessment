from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from utils.notifications import send_order_sms, send_order_email_to_admin

@receiver(post_save, sender=Order)
def handle_new_order(sender, instance, created, **kwargs):
    if created:
        # Send SMS to customer
        if instance.customer.phone_number:
            send_order_sms(instance.customer.phone_number, instance.id)
        
        # Send email to admin
        send_order_email_to_admin(instance)