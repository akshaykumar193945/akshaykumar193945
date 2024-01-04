function forgetPassword(){

    fetch('/forgot_password').then(response => response.text())
        .then(data => {
            // Insert the fetched content into the 'content' div
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading "find" content:', error);
        });
};

function submitPwdRecoveryForm(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    console.log("inside password recovery : ", username, " ::::: ");
    fetch(`/update_password_1/${username}`)
        .then(response => response.text())
        .then(data => {
            // Insert the fetched content into the 'content' div
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading "update_password" content:', error);
        });
};

function submitUpdatedPwd(username) {
    event.preventDefault();
    console.log("in in in in in in in ");

    // Create the line break element
    var lineBreak = document.createElement("br");

    // "Iterate over the form data of class='new-pwd-form' "
    const formData = new FormData(document.querySelector('.new-pwd-form'));
    const formDataObject = {};
    formData.forEach((value, key) => {
        formDataObject[key] = value;
    });

    var newPasswordInput = document.getElementById('new_password');
    var newPasswordError = document.getElementById('newPasswordError');
    var confirmNewPassword = document.getElementById('confirmNewPassword');
    var oneBreakContainer = document.getElementById('oneBreak');
    var oneBreak_1_Container = document.getElementById('oneBreak_1');
    

    var confirmPasswordInputError = document.getElementById('confirmNewPasswordError');

    // Event listener to clear the error message and remove the line break
    newPasswordInput.addEventListener('focus', function () {
        newPasswordError.innerHTML = '';
        // console.log("hjhjhjhjhjhh");
        if (oneBreakContainer.contains(lineBreak)) {
            oneBreakContainer.removeChild(lineBreak);
            console.log("hjhjhjhjhjhh");
        }
    });
    
    confirmNewPassword.addEventListener('focus', function () {
        confirmNewPasswordError.innerHTML = '';
        // console.log("hjhjhjhjhjhh");
        if (oneBreak_1_Container.contains(lineBreak)) {
            oneBreak_1_Container.removeChild(lineBreak);
            console.log("hjhjhjhjhjhh");
        }
    });        
    
    console.log(newPasswordInput.value, confirmNewPassword.value);
    fetch(`/password_updated/${username}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formDataObject),
    })
    .then(response => response.json())
    .then(data => {
        console.log('7777777777777777777');
        console.log(data.status);
        if (data.status == true && data.status !== '1') {
            console.log(data.message);
            // document.getElementById('content').innerHTML = `Password Updated: ${JSON.stringify(data.user_password)}`;
            // Other actions you want to perform on success
            myDialog(`Password Updated: ${JSON.stringify(data.user_password)} Succesfully`, function () {loadLoginPage();});

            // loadLoginPage();
        } else if (data.status === '1') {
            console.warn(data.message);
            confirmPasswordInputError.innerHTML = data.message;
            oneBreak_1_Container.appendChild(lineBreak);
        } else {
            console.error(data.message);
            newPasswordError.innerHTML = data.message;
            oneBreakContainer.appendChild(lineBreak);
        }
    })
    .catch(error => {
        console.error('Error loading "update_password" content:', error);
    });
};