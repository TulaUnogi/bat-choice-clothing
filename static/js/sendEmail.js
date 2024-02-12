function sendMail(contactForm) {
    emailjs.send("gmail", "bat-choice-contact", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.emailaddress.value,
        "message": contactForm.message.value
    })
    .then(
        function(response) {
            console.log("MESSAGE SENT SUCCESSFULLY", response);
        },
        function(error) {
            console.log("MESSAGE SENDING FAILED", error);
        }
    );
    return alert("Message has been sent!")
}