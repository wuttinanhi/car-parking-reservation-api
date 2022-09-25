async function main() {
  const request = await fetch("payment/stripe/public_key");
  const public_key = await request.text();
  console.log(public_key);

  var stripe = Stripe(public_key);

  var elements = stripe.elements();

  // Set up Stripe.js and Elements to use in checkout form
  var style = {
    base: {
      color: "#32325d",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#aab7c4",
      },
    },
    invalid: {
      color: "#fa755a",
      iconColor: "#fa755a",
    },
  };

  var cardElement = elements.create("card", { style: style });
  cardElement.mount("#card-element");

  var submitButton = document.getElementById("submit");

  submitButton.addEventListener("click", (event) => {
    var clientSecret = document.getElementById("client_secret").value;
    console.log(clientSecret);

    stripe
      .confirmCardPayment(clientSecret, {
        payment_method: {
          card: cardElement,
        },
      })
      .then(function (result) {
        console.log(result);
        if (result.error) {
          // Inform the customer that there was an error.
          console.log(result.error);
          // alert(result.error);
        }
      });
  });
}

main();
