function pickSong(song) {
    console.log(song);
    fetch('/send_music/' + song)
        .catch(error => {
        console.error('Error:', error);
    });
    window.location.href = "/sing";
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
    window.location.href = "/music-list";
}

function openModalTerms() {
    const overlay = document.querySelector(".overlay");

    overlay.classList.remove("remove-overlay");
}

function closeModalTerms() {
    const overlay = document.querySelector(".overlay");

    overlay.classList.add("remove-overlay");
}
