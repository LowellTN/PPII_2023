function processDonation() {
    var amount = document.getElementById('amount').value;
    var name = document.getElementById('name').value;

    // Traitement des dons

    displayThankYouMessage(name);
}

function displayThankYouMessage(name) {
    var donationForm = document.getElementById('donation-form');
    var thankYouSection = document.getElementById('thank-you');
    donationForm.style.display = 'none';
    thankYouSection.style.display = 'block';
    thankYouSection.innerHTML = `<h2>Merci, ${name} !</h2>
                                <p>Votre don a été reçu avec gratitude. Merci pour votre soutien.</p>`;
}
