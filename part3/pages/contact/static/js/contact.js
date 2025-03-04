document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".contact-form").addEventListener("submit", async function (event) {
        event.preventDefault(); // מניעת רענון העמוד כברירת מחדל

        let formData = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            phone: document.getElementById("phone").value,
            message: document.getElementById("message").value
        };

        try {
            let response = await fetch("/contact/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });

            let result = await response.json();
            if (result.success) {
                alert("Your message has been sent successfully!");
                document.querySelector(".contact-form").reset();
            } else {
                alert("Error: " + result.error);
            }
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("Something went wrong. Please try again.");
        }
    });
});
