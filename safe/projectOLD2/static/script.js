function loading() {
    document.querySelector(".add-form").style.display="none";
    document.querySelector(".loading").style.display="block";
}

const repeatBtn = document.querySelector(".repeat");
repeatBtn.addEventListener("click", () => {
        repeatBtn.classList.toggle("activeButton")
});

