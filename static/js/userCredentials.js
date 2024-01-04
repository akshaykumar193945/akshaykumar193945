// JavaScript to load "user_credential" section using AJAX
// document.getElementById('load-user-credential').addEventListener('click', function(e) {
    function loadUserCredential(){
        console.log("in user record ###########");
        fetch('/user_records')
            .then(response => response.text())
            .then(data => {
                // Insert the fetched content into the 'content' div
                console.log("in user_records");
                document.getElementById('content').innerHTML = data;
            })
            .catch(error => {
                console.error('Error loading "find" content:', error);
            });
    };

    function updateUserRecord(recordId) {
        if (confirm('Are you sure you want to update this record?')) {
            fetch(`/update_user_record/${recordId}`)
                .then(response => response.text())
                .then(data => {
                    // Insert the fetched content into the 'content' div
                    console.log("in edit user record ");
                    document.getElementById('content').innerHTML = data;
                })
                .catch(error => {
                    console.error('Error loading "find" content:', error);
                });
        }
    };

    function submitUpdateUserData(recordId) {
        event.preventDefault();
        if (validateUserForm()) {
            var formData = {
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                mobile_number: document.getElementById('mobile_number').value,
            };
            if (confirm('Are you sure you want to update this record ??')) {
                event.preventDefault();
                console.log('in record user edited');
                fetch(`/record_user_edited/${recordId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Set the Content-Type header
                    },
                    body: JSON.stringify(formData),
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Failed to update record');
                    }
                })
                .then(data => {
                    console.log(data.message);
                    if (data.user_record) {
                        // document.getElementById('content').innerHTML = `Updated User Record: ${JSON.stringify(data.user_record)}`;
                        myDialog(`Updated User Record: ${JSON.stringify(data.user_record)}`, function() {loadUserCredential();});                        
                    } else {
                        console.log('No updated record information provided');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        }
        return false;
    };

    function validateUserForm(){
        // add your form validation here
    return true;
    }

    function deleteUserRecord(recordId) {
        if (confirm('Are you sure you want to delete this record?')) {
            fetch(`/delete_user_record/${recordId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Failed to delete record');
                }
            })
            .then(data => {
                // Handle successful deletion, e.g., update UI or show a message
                console.log(data.message);
                if (data.deleted_record) {
                    // document.getElementById('content').innerHTML = `Deleted Record: ${JSON.stringify(data.deleted_record)}`;
                    myDialog(`Deleted Record: ${JSON.stringify(data.deleted_record)}`, function () {loadUserCredential();});
                    // loadUserCredential();
                } else {
                    // Handle the case where no deleted record information is returned
                    console.log('No deleted record information provided');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    };