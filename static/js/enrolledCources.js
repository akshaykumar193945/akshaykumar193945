function goToCourse(){
    console.log("i am in course page ")
    fetch('/courses')
        .then(response => response.text())
        .then(data => {
            // Insert the fetched content into the 'content' div
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading "find" content:', error);
        });
};

function enrollCourse(event, course, course_id) {
    event.preventDefault(); // Prevent the default link behavior

    // Use fetch to check login status
    fetch('/check_login_status')
        .then(response => response.json())
        .then(data => {
            // Check if the user is authenticated
            if (data.authenticated) {
                // If authenticated, proceed to fetch and load course content
                console.log("In enroll courses !!! ");
                fetch(`/enroll_Course`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ course_name : course, course_id : course_id }), // Include the selected course data
                })
                .then(response => response.json())
                .then(courseData => {
                    // Insert the fetched content into the 'content' div
                    //document.getElementById('content').innerHTML = courseData;
                console.log("In enroll courses In enroll courses !!! ");
                console.log(courseData);
                if (courseData.status == true){
                    myDialog(`Enrolled successful: ${JSON.stringify(courseData.message)}`, function () { userProfile();});
                } else{                        
                    console.warn(courseData.message);
                    myDialog(`${JSON.stringify(courseData.message)}`, function () { userProfile();});
                }
                })
                .catch(courseError => {
                    console.error('Error loading "enroll Course" content:', courseError);
                });
            } else {
                // If not authenticated, redirect to the login page
                console.log("not authenticated ");
                alert("Please login to Enroll in your cource ");
                document.getElementById('content').innerHTML = loadLoginPage()
            }
        })
        .catch(error => {
            console.error('Error checking login status:', error);
        });
};


function showEnrolledCourse(){
		
    fetch('/show_enrolled_course').then(response => response.text())
        .then(data => {
            // Insert the fetched content into the 'content' div
            console.log("in cources !!!!!!!!");
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading "find" content:', error);
        });
};

function updateUserOrder(recordId){
    if (confirm('Are you sure you want to update this record?')) {
        fetch(`/edit_user_order/${recordId}`)
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

function submitUpdateUserOrder(event, recordId) {
    event.preventDefault();
    if (validateUserForm()) {
       var formData = {
           course: document.getElementById('course').value,
           course_id: document.getElementById('course_id').value,
       };
       if (confirm('Are you sure you want to update this record ??')) {
           console.log('in edit user order', formData);
           fetch(`/submit_edit_order/${recordId}`, {
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
                   throw new Error('Failed to update order');
               }
           })
           .then(data => {
               console.log(data.message);
               if (data.user_order) {
                //    document.getElementById('content').innerHTML = `Updated User order: ${JSON.stringify(data.user_order)}`;
                   myDialog(`Updated User order: ${JSON.stringify(data.user_order)}`, function(){showEnrolledCourse();});
                   
               } else {
                   console.log('No updated order information provided');
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

function deleteUserOrder(recordId) {
    if (confirm('Are you sure you want to delete this order?')) {
        fetch(`/delete_user_order/${recordId}`, {
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
                // document.getElementById('content').innerHTML = `Deleted Order: ${JSON.stringify(data.deleted_record)}`;
                myDialog(`Deleted Order: ${JSON.stringify(data.deleted_record)}`, function () {showEnrolledCourse();});
                // showEnrolledCourse();
            } else {
                // Handle the case where no deleted record information is returned
                console.log('No deleted record information provided');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
