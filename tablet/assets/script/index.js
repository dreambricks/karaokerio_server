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
