function pickSOng(song) {
  console.log(song);
  location.replace("/tablet/termos.html");
}

function checkPrivacy() {
  const isPrivateChecked = document.querySelector("#privacy");

  if (isPrivateChecked.checked) {
    document.querySelector(".sing").disabled = false;
    return;
  }
  document.querySelector(".sing").disabled = true;
}

function singSong() {
  location.replace("/tablet/cantar.html");
}

function openModalTerms() {
  const overlay = document.querySelector(".overlay");

  overlay.classList.remove("remove-overlay");
}

function closeModalTerms() {
  const overlay = document.querySelector(".overlay");

  overlay.classList.add("remove-overlay");
}

const termsBox = document.querySelector(".terms ");

if (termsBox) {
  termsBox.addEventListener("scroll", function () {
    const scrollTop = termsBox.scrollTop;
    const scrollHeight = termsBox.scrollHeight;
    const clientHeight = termsBox.clientHeight;

    if (scrollTop + clientHeight >= scrollHeight) {
      document.querySelector("#privacy").disabled = false;
    }
  });
}
