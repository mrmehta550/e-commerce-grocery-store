from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_order_status_email(order, request):

    subject = f"Order #{order.id} Update"

    # 🔗 Tracking URL
    tracking_url = request.build_absolute_uri(
        f"/orders/tracking/{order.id}/"
    )

    # Render HTML
    html_content = render_to_string(
        'emails/order_status.html',
        {
            'order': order,
            'tracking_url': tracking_url
        }
    )

    email = EmailMultiAlternatives(
        subject,
        "Your order status updated",
        settings.EMAIL_HOST_USER,
        [order.email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()