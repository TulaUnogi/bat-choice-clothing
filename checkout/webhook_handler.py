from django.http import HttpResponse


class Stripe_Webhook_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_webhook_event(self, event):
        """
        Handle various webhook events
        """
        return HttpResponse(
            content=f'Received a webhook: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle successful payment intent webhook
        """
        intent = event.data.object
        print(intent)
        return HttpResponse(
            content=f'Received a webhook: {event["type"]}',
            status=200)

    def handle_payment_intent_failed(self, event):
        """
        Handle unsuccessful payment intent webhook
        """
        return HttpResponse(
            content=f'Received a webhook: {event["type"]}',
            status=200)