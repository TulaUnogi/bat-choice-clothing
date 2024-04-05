/*
    Main logic & payment flow from:
    https://stripe.com/docs/payments/accept-a-payment
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements({
    fonts: [
      {
        // integrate your font into stripe
        cssSrc: 'https://fonts.googleapis.com/css2?family=Megrim&family=Montserrat:ital,wght@0,100;0,400;0,700;1,400&display=swap',
      }
    ]
  });;

var style = {
    base: {
        color: '#495057',
        fontSmoothing: 'antialiased',
        fontFamily: '"Montserrat", sans-serif',
        fontWeight: '400',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4',
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');


/* Card validation errors handling */

card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});
