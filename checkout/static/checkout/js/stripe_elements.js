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
        // integrate font into stripe
        cssSrc: 'https://fonts.googleapis.com/css2?family=Megrim&family=Montserrat:ital,wght@0,100;0,400;0,700;1,400&display=swap',
      }
    ]
  });

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


// Card validation errors handling

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

// Form submission handling
var form = document.getElementById('pay_form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#pay_form').fadeToggle(100);
    $('#checkout-loading').fadeToggle(100);

    var infoSave = Boolean($('#info_save').attr('checked'));
    // from {% csrf_token %} in form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'info_save': infoSave,
    };
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function(){
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.first_name.value + form.last_name.value),
                    email: $.trim(form.email.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.address_line1.value),
                        line2: $.trim(form.address_line2.value + form.address_line3.value),
                        state: $.trim(form.region.value),
                        city: $.trim(form.city.value),
                        postal_code: $.trim(form.postcode.value),
                        country: $.trim(form.country.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.first_name.value + form.last_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.address_line1.value),
                    line2: $.trim(form.address_line2.value + form.address_line3.value),
                    state: $.trim(form.region.value),
                    city: $.trim(form.city.value),
                    postal_code: $.trim(form.postcode.value),
                    country: $.trim(form.country.value),
                }                
            },
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#pay_form').fadeToggle(100);
                $('#checkout-loading').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function() {
        // Reload the page if fails
        location.reload();
    });
});