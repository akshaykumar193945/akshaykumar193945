
// function sendOTP() {
//     const email = document.getElementById('email').value;
//     console.log('in sendOtp');
//     console.log(email);
//     // Make a fetch request to send OTP
//     fetch('/send_otp', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ email: email }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         verification_status_msg = document.getElementById('email-verification-icon')
//         sendOtpContainer = document.getElementById('sendOtpContainer') 
//         if (data.status){
//             console.log(data.message);
//             sendOtpContainer.style.display = 'none';
//             document.getElementById('otpContainer').style.display = 'block';
//         } else {
//             console.warn(data.error);
//             verification_status_msg.style.display = 'block';
//             verification_status_msg.style.color = 'red';
//             verification_status_msg.innerHTML = data.error;
//         }
//         // Display OTP input field
//     })
//     .catch(error => {
//         console.error('Error sending OTP:', error);
//     });
// }

// function verifyOTP() {
//     const enteredOTP = document.getElementById('otp').value;
    
//     // Make a fetch request to verify OTP
//     fetch('/verify_otp', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ otp: enteredOTP }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('sendOtpContainer').style.display = 'none'; 
//         verification_status_msg = document.getElementById('email-verification-icon') 
//         // btnVerifyOTP = document.getElementById('btn-verifyOTP')
//         // otpContainer = document.getElementById('otpContainer')sendOtpContainer
//         sendOtpContainer = document.getElementById('sendOtpContainer');
//         otpContainer = document.getElementById('otpContainer');

//         otpForm = document.getElementById('otpForm') 
        
//         if (data.status){
//             console.log(data.message);
//             verification_status_msg.innerHTML = '<p>Verified</p>';                
//             verification_status_msg.style.display = 'block';                
//             verification_status_msg.style.color = 'green'; 
//             sendOtpContainer.style.display = 'none'; 
//             otpContainer.style.display = 'none';  
//             // otpForm.style.display = 'none'

//         } else {
//             console.warn(data.error);
//             verification_status_msg.innerHTML = '<p>Invalid OTP !</p>';                
//             verification_status_msg.style.display = 'block';              
//             verification_status_msg.style.color = 'red';                
//             // btnVerifyOTP.style.display = 'none';                
//             // otpContainer.style.display = 'none';   
//             // document.getElementById('btn-sendOtp').style.display = 'block'; 
//             document.getElementById('sendOtpContainer').style.display = 'block'; 
//             document.getElementById('btn-sendOtp').innerHTML = 'Re-Send'; 
//             document.getElementById('otpContainer').style.display = 'none'; 

//         }
//     })
//     .catch(error => {
//         console.error('Error verifying OTP:', error);
//     });
// }

// Constants for selectors

// const emailInput = document.getElementById('email');
// const sendOtpContainer = document.getElementById('sendOtpContainer');
// const otpContainer = document.getElementById('otpContainer');
// const verificationStatusMsg = document.getElementById('email-verification-icon');

// // Function to send OTP
// async function sendOTP() {
//     try {
//         const email = emailInput.value;
//         const response = await fetch('/send_otp', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ email }),
//         });
//         const data = await response.json();

//         if (data.status) {
//             console.log(data.message);
//             toggleDisplay(sendOtpContainer, 'none');
//             toggleDisplay(otpContainer, 'block');
//         } else {
//             console.warn(data.error);
//             displayError(data.error);
//         }
//     } catch (error) {
//         console.error('Error sending OTP:', error);
//     }
// }

// // Function to verify OTP
// async function verifyOTP() {
//     try {
//         const enteredOTP = document.getElementById('otp').value;
//         const response = await fetch('/verify_otp', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ otp: enteredOTP }),
//         });
//         const data = await response.json();

//         if (data.status) {
//             console.log(data.message);
//             displaySuccess('Verified');
//             hideElements([sendOtpContainer, otpContainer]);
//         } else {
//             console.warn(data.error);
//             displayError('Invalid OTP !');
//             showElements([sendOtpContainer], [otpContainer]);
//             document.getElementById('btn-sendOtp').innerHTML = 'Re-Send';
//         }
//     } catch (error) {
//         console.error('Error verifying OTP:', error);
//     }
// }

// // Utility function to toggle display
// function toggleDisplay(element, displayValue) {
//     element.style.display = displayValue;
// }

// // Utility function to display success message
// function displaySuccess(message) {
//     verificationStatusMsg.innerHTML = `<p>${message}</p>`;
//     verificationStatusMsg.style.display = 'block';
//     verificationStatusMsg.style.color = 'green';
// }

// // Utility function to display error message
// function displayError(error) {
//     verificationStatusMsg.innerHTML = `<p>${error}</p>`;
//     verificationStatusMsg.style.display = 'block';
//     verificationStatusMsg.style.color = 'red';
// }

// // Utility function to show elements and hide others
// function showElements(show, hide) {
//     show.forEach(element => toggleDisplay(element, 'block'));
//     hide.forEach(element => toggleDisplay(element, 'none'));
// }

// // Utility function to hide elements
// function hideElements(elements) {
//     elements.forEach(element => toggleDisplay(element, 'none'));
// }

// // Add event listeners
// document.getElementById('btn-sendOtp').addEventListener('click', sendOTP);
// document.getElementById('btn-verifyOTP').addEventListener('click', verifyOTP);

function sendOTP() {
    const email = document.getElementById('email').value;
  
    // Make a fetch request to send OTP
    fetch('/send_otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: email }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.status) {
        console.log(data.message);
  
        // Hide email input and show OTP fields
        document.getElementById('sendOtpContainer').style.display = 'none';
        document.getElementById('otpContainer').style.display = 'block';
  
        // Focus on the first OTP input field for better user experience
        document.getElementById('otp').focus();
      } else {
        console.warn(data.error);
        displayErrorMessage(data.error);
      }
    })
    .catch(error => {
      console.error('Error sending OTP:', error);
      displayErrorMessage('Failed to send OTP. Please try again.');
    });
  }
  
  function verifyOTP() {
    const enteredOTP = document.getElementById('otp').value;
  
    // Make a fetch request to verify OTP
    fetch('/verify_otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ otp: enteredOTP }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.status) {
        console.log(data.message);
        displaySuccessMessage('Verified');
        // Proceed with further actions after successful verification
      } else {
        console.warn(data.error);
        displayErrorMessage(data.error);
      }
    })
    .catch(error => {
      console.error('Error verifying OTP:', error);
      displayErrorMessage('Failed to verify OTP. Please try again.');
    });
  }
  
  // Helper function to display error/success messages
  function displayErrorMessage(message) {
    const verificationStatusMsg = document.getElementById('email-verification-icon');
    verificationStatusMsg.style.display = 'block';
    verificationStatusMsg.style.color = 'red';
    verificationStatusMsg.innerHTML = message;
  }
  
  function displaySuccessMessage(message) {
    const sendOtpContainer = document.getElementById('sendOtpContainer');
    const otpContainer = document.getElementById('otpContainer');
    const verificationStatusMsg = document.getElementById('email-verification-icon');
    verificationStatusMsg.style.display = 'block';
    verificationStatusMsg.style.color = 'green';
    verificationStatusMsg.innerHTML = message;
    sendOtpContainer.style.display = 'none'
    otpContainer.style.display = 'none'
  }
  
