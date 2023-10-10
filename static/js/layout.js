const account = document.querySelector(".account-info");
const bookings = document.querySelector(".bookings");

account.addEventListener("click", () => {
  bookings.classList.toggle("show-bookings");
});

const side_account = document.querySelector(".side-account");
const burger = document.querySelector(".burger");

burger.addEventListener("click", () => {
  side_account.classList.toggle("show-side");
});
