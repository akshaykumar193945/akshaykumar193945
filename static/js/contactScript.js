        // JavaScript to load "contact" section using AJAX
function contactForm() {
    // Use AJAX to fetch the "About" section content
    fetch('/contact')
        .then(response => response.text())
        .then(data => {
            // Insert the fetched content into the 'content' div
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading "contact" content:', error);
        });
}

function showContact(){
    console.log("i am in separte js file but included in layout.html");
    fetch(`/contact_records`)
        .then(response => response.text())
        .then(data => {
            // Insert the fetched content into the 'content' div
            console.log("in contact_records");
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading "find" content:', error);
            }
        );
};

function onContactSubmit(event) {
    event.preventDefault();
    const formData = new FormData(document.querySelector('#contactForm'));

    // Create an object from the form data
    const formDataObject = {};
    formData.forEach((value, key) => {
        formDataObject[key] = value;
    });

    // Convert the object to a JSON string
    const jsonData = JSON.stringify(formDataObject);
    console.log(jsonData)
    console.log("Submitting contact form");

    // Replace 'YOUR_API_ENDPOINT' with your actual API endpoint
    fetch(`/contact_submission`, {
        method: 'POST', // or 'PUT', 'DELETE', etc.
        headers: {
            'Content-Type': 'application/json',
            // Add any other headers you may need, e.g., authorization headers
        },
        body: jsonData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON from the response
    })
    .then(data => {
        console.log('Server response:', data);
        myDialog(`${JSON.stringify(data.message)}`, function () { loadLoginPage();});
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });
};

function updateContactRecord(contactId){
    if (confirm('Are you sure you want to Update this Contact?')) {
        console.log("in update contact form");
        console.log(contactId);

        var contactId = {
            contactId: contactId,
        };
        var jsonString = JSON.stringify(contactId);
        console.log(jsonString);
        fetch(`/update_contact`,  {
            method: 'POST',            
            headers: {
                'Content-Type': 'application/json',
            },
            body: jsonString,
        })            
        .then(response => response.text())
        .then(data => {
            // Insert the fetched content into the 'content' div
            console.log("in contact_records");
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading "find" content:', error);
            }
        );
    }
};

function submitUpdateContact(contactId) {
    event.preventDefault();
    if (confirm('Are you sure you want to Delete this Contact?')) {
        const formData = new FormData(document.querySelector('.update-contact-form'));
        const formDataObject = {};
        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });

        formDataObject['contactId'] = contactId;
        // console.log(formDataObject['contactId'] );

        // Convert the object to a JSON string
        const jsonData = JSON.stringify(formDataObject);
        
        fetch(`/execute_update_contact`,  {
            method: 'POST',            
            headers: {
                'Content-Type': 'application/json',
            },
            body: jsonData,
        })            
        .then(response => response.json())
        .then(data => {
            if (data.status){
                console.log("in execute contact_records");
                console.log(data.message);
                myDialog(`${JSON.stringify(data.message)} Updated`, function () {showContact();});
            }
            else{
                console.log(data.message);
                myDialog(`${JSON.stringify(data.message)}`, function () {showContact();});
            }
        })
        .catch(error => {
            console.error('Error loading content:', error);
            console.log(data.message);
            }
        )
    }
};

function deleteContactRecord(contactId){
    if (confirm('Are you sure you want to Delete this Contact?')) {
        console.log("in delete delete");
        console.log(contactId);

        var contactId = {
            contactId: contactId,
        };

        // Convert the JavaScript object to a JSON string
        var jsonString = JSON.stringify(contactId);

        // Output the JSON string
        console.log(jsonString);
        fetch(`/delete_contact`,  {
            method: 'POST',            
            headers: {
                'Content-Type': 'application/json',
            },
            body: jsonString,
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
                if (data.deleted_contact) {
                    // document.getElementById('content').innerHTML = `Deleted Record: ${JSON.stringify(data.deleted_record)}`;
                    myDialog(`Deleted Record: ${JSON.stringify(data.deleted_contact)}`, function () {showContact();});
                    // loadUserCredential();
                } else {
                    // Handle the case where no deleted record information is returned
                    console.log('No deleted record information provided'+ (data.error ?? ''));
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
};