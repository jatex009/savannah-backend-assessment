import africastalking
from django.core.mail import send_mail
from django.conf import settings
from decouple import config

# Initialize Africa's Talking
username = config('AFRICAS_TALKING_USERNAME', default='sandbox')
api_key = config('AFRICAS_TALKING_API_KEY', default='')


# DEBUG: Print what credentials are being used
print(f"DEBUG: Using AT username: {username}")
print(f"DEBUG: API key exists: {bool(api_key)}")
print(f"DEBUG: API key first 8 chars: {api_key[:8] if api_key else 'None'}")


if api_key:
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS

def send_order_sms(phone_number, order_id):
    """Send SMS notification to customer"""
    if not api_key:
        print(f"SMS would be sent to {phone_number}: Order #{order_id} confirmed!")
        return {"status": "simulated"}
    
    message = f"Hello! Your order #{order_id} has been placed successfully. Thank you!"
    
    try:
        response = sms.send(message, [phone_number])
        print(f"SMS sent to {phone_number} for order #{order_id}")
        return response
    except Exception as e:
        print(f"SMS Error: {e}")
        return {"error": str(e)}

def send_order_email_to_admin(order):
    """Send email notification to admin"""
    subject = f"New Order Placed - #{order.id}"
    
    items_list = "\n".join([
        f"- {item.quantity}x {item.product.name} @ ${item.price} = ${item.subtotal}"
        for item in order.items.all()
    ])
    
    message = f"""
New order details:
=================
Order ID: {order.id}
Customer: {order.customer.username} ({order.customer.email})
Phone: {order.customer.phone_number}
Total Amount: ${order.total_amount}

Items Ordered:
{items_list}

Order placed at: {order.created_at}
    """
    
    try:
        send_mail(
            subject,
            message,
            config('EMAIL_HOST_USER', default='noreply@ecommerce.com'),
            [config('ADMIN_EMAIL', default='admin@ecommerce.com')],
            fail_silently=False,
        )
        print(f"Admin email sent for order #{order.id}")
    except Exception as e:
        print(f"Email Error: {e}")



