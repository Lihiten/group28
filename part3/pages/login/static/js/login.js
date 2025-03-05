document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".login-form");
    const flashMessageContainer = document.querySelector(".flashes");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // מונע טעינה מחדש של הדף

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!email || !password) {
            displayMessage("All fields are required!", "error");
            return;
        }

        try {
            const response = await fetch("/login/login", {  // וודא שהנתיב נכון!
                method: "POST",
                headers: {
                    "Content-Type": "application/json"  // 📌 חשוב! מוודא שהבקשה היא JSON
                },
                body: JSON.stringify({ email, password })  // 📌 הופך את הנתונים ל- JSON
            });

            const result = await response.json();
            console.log("🔹 Server response:", result);  // 🔍 נבדוק מה השרת מחזיר

            if (result.success) {
                window.location.href = result.redirect || "/workshops/";
            } else {
                displayMessage(result.message, "error");
            }
        } catch (error) {
            console.error("Error during login:", error);
            displayMessage("An unexpected error occurred. Please try again.", "error");
        }
    });

    function displayMessage(message, type) {
        flashMessageContainer.innerHTML = "";
        const errorMessage = document.createElement("li");
        errorMessage.classList.add(type);
        errorMessage.textContent = message;
        flashMessageContainer.appendChild(errorMessage);
    }
});
