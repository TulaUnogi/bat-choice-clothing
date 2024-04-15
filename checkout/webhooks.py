from django.conf import settings
from django.http import HttpResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import Stripe_Webhook_Handler
import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """ Listen to Stripe webhooks """
    
    # Setup
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get and verify the webhook data and signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # When there's an invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # When there's an invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # Set up a webhook handler
    handler = Stripe_Webhook_Handler(request)

    # Map webhook events to the right handlers
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type
    event_type = event['type']

    """ Get a handler from the event map
    or use the generic one by default """
    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    print('success!')
    return response