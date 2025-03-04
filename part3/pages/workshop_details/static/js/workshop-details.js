document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript Loaded!");

    // Get the workshop type from the URL
    const pathSegments = window.location.pathname.split("/");
    const type = pathSegments[pathSegments.length - 1];

    console.log("📢 Detected Workshop Type:", type);

    // Workshop details
    const workshops = {
        italian: {
            title: "Italian Cooking Workshop",
            description: "Master the art of fresh pasta, creamy risotto, and classic Margherita pizza.",
            menu: ["Homemade Pasta", "Risotto alla Milanese", "Classic Margherita Pizza", "Tiramisu"],
            times: ["7:30 PM", "8:30 PM", "9:30 PM"]
        },
        asian: {
            title: "Asian Cuisine Workshop",
            description: "Roll sushi, cook rich ramen, and stir-fry like a pro!",
            menu: ["Sushi Rolls", "Ramen Noodles", "Stir-Fried Vegetables", "Miso Soup"],
            times: ["7:30 PM", "8:30 PM", "9:30 PM"]
        },
    };

    // Find the selected workshop
    const workshop = workshops[type];
    const detailsContainer = document.getElementById("workshop-details");

    if (!detailsContainer) {
        console.error("❌ Workshop details container NOT FOUND!");
        return;
    }

    console.log("✅ Workshop details container FOUND!");

    if (workshop) {
        detailsContainer.innerHTML = `
            <section class="workshop-header">
                <h1>${workshop.title}</h1>
                <p>${workshop.description}</p>
            </section>
            <section class="menu-section">
                <h2>Menu</h2>
                <ul>${workshop.menu.map(item => `<li>${item}</li>`).join("")}</ul>
            </section>
            <section class="registration-section">
                <h2>Register for the Workshop</h2>
                <form id="registration-form">
                    <label for="date">Choose a Date:</label>
                    <input type="date" id="date" required>

                    <label for="time">Choose a Time:</label>
                    <select id="time">${workshop.times.map(time => `<option>${time}</option>`).join("")}</select>

                    <label for="participants">Number of Participants:</label>
                    <input type="number" id="participants" min="1" max="10" required>

                    <button type="submit" class="button">Register</button>
                </form>
            </section>
        `;

        // Restrict date selection
        const dateInput = document.getElementById("date");
        if (dateInput) {
            const today = new Date().toISOString().split("T")[0];
            dateInput.setAttribute("min", today);
        }

        // Handle form submission
        const form = document.getElementById("registration-form");
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            const date = document.getElementById("date").value;
            const time = document.getElementById("time").value;
            const participants = document.getElementById("participants").value;

            checkLoginStatus(() => {
                registerWorkshop(workshop.title, date, time, participants);
            });
        });
    } else {
        detailsContainer.innerHTML = `<h1>Workshop not found</h1>`;
    }
});

// Check if user is logged in before registration
function checkLoginStatus(callback) {
    fetch("/auth/check_login_status")
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                alert("You must be logged in to register for a workshop!");
                window.location.href = "/login/login";
            } else {
                callback();
            }
        })
        .catch(error => console.error("Error:", error));
}

// Register for the workshop
function registerWorkshop(workshop, date, time, participants) {
    fetch("/workshop_details/register_workshop", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ workshop, date, time, participants })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = `/summary?workshop=${encodeURIComponent(workshop)}&date=${date}&time=${time}&participants=${data.participants}`;
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript Loaded, Waiting for Register Button Click...");

    const registerButton = document.querySelector(".button");
    if (!registerButton) {
        console.error("❌ Register button not found!");
        return;
    }

    registerButton.addEventListener("click", function () {
        console.log("🚀 Register Button Clicked!");
    });
});
