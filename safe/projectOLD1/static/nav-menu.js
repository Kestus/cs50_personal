const navToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector(".nav-menu");

navToggle.addEventListener("click", () => {
    const visible = navMenu.getAttribute("data-visible");

    if(visible === "False")
    {
        navMenu.setAttribute("data-visible", "True")
        navToggle.setAttribute("data-visible", "True")
    }
    else
    {
        navMenu.setAttribute("data-visible", "False")
        navToggle.setAttribute("data-visible", "False")
    }
});