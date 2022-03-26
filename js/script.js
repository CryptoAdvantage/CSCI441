document.querySelector(".menu-btn").addEventListener("click", (e) => {
    e.currentTarget.classList.toggle("open")
    document.querySelector("div.name").classList.toggle("open")
    document.querySelector("div.menu").classList.toggle("open")
    document.querySelector("nav").classList.toggle("open")
}, false)