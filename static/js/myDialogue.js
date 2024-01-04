var directedFunct;
function showFloatingDialog(message) {
    var dialog = document.getElementById('floating-dialog');
    var content = document.getElementById('dialog-content');
    content.innerHTML = message;
    dialog.style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}

function closeDialog() {
    var dialog = document.getElementById('floating-dialog');
    dialog.style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
    // Restore scrolling when the overlay is closed
    document.body.style.overflow = 'auto';
    directedFunct();
}

// Simulate a server response
function myDialog(serverResponse, callBack) {
    // Use setTimeout to simulate a delay before showing the dialog
    setTimeout(function () {
        console.log(serverResponse); // Log the server response to the console
        showFloatingDialog(serverResponse); // Show the floating dialog with the server response
        // Disable scrolling when the overlay is active
        document.body.style.overflow = 'hidden';
        directedFunct = callBack;
    }, 500);  // Simulating a delay of .5 seconds
}