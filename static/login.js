var box = document.querySelector(".box");
var box1 = document.querySelector(".box1");
var sign = document.querySelector(".sign");
var login1 = document.querySelector(".login1");

sign.addEventListener("click", () => {
  box1.style.display = "block";
  login1.style.display = "block";
  box.style.display = "none";
  sign.style.display = "none";
});

login1.addEventListener("click", () => {
  box1.style.display = "none";
  login1.style.display = "none";
  box.style.display = "block";
  sign.style.display = "block";
});
