function client_side_validation() {
    var nameField = document.getElementById("name");
    var nameValue = nameField.value;
    var pattern = /^[a-zA-Z0-9 ]+$/; // Allow only letters, numbers, and spaces
    if (!pattern.test(nameValue)) {
        alert("Please enter a valid name without special characters.");
        nameField.value = ""; // Clear the input field
    }
}
