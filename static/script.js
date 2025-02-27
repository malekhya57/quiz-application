const API_URL = "http://127.0.0.1:5000";

function register() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("Please enter both username and password!");
        return;
    }

    fetch(`${API_URL}/auth/register_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.message.includes("success")) {
            window.location.href = "/";  // Redirect to login page
        }
    })
    .catch(error => console.error("Error:", error));
}

function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("Please enter both username and password!");
        return;
    }

    fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            alert("Login successful!");
            window.location.href = "/quiz";  // Redirect to quiz page
        } else {
            alert("Invalid username or password");
        }
    })
    .catch(error => console.error("Error:", error));
}
