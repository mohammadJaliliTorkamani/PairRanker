document.querySelectorAll(".survey-form").forEach(form => {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        await fetch("/submit", {
            method: "POST",
            body: formData
        });

        form.innerHTML = "<p>Submitted ✔</p>";
    });
});