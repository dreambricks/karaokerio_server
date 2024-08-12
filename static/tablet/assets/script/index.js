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
