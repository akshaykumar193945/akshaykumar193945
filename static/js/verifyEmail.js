
// Function to make a fetch request
async function makeRequest(url, method, body) {
  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Error: ${error}`);
    throw error;
  }
}

// Function to send OTP
async function sendOTP() {
  try {
    const email = document.getElementById('email').value;
    const data = await makeRequest('/send_otp', 'POST', { email });

    if (data.status) {
      console.log(data.message);
      handleOTPVerification(true);
    } else {
      console.warn(data.error);
      handleOTPVerification(false, data.error);
    }
  } catch (error) {
    console.error('Error sending OTP:', error);
    handleOTPVerification(false, 'Failed to send OTP. Please try again.');
  }
}

// Function to verify OTP
async function verifyOTP() {
  try {
    const enteredOTP = document.getElementById('otp').value;
    const data = await makeRequest('/verify_otp', 'POST', { otp: enteredOTP });

    if (data.status) {
      console.log(data.message);
      displaySuccessMessage('Verified');
      // Proceed with further actions after successful verification
    } else {
      console.warn(data.error);
      displayErrorMessage(data.error);
    }
  } catch (error) {
    console.error('Error verifying OTP:', error);
    displayErrorMessage('Failed to verify OTP. Please try again.');
  }
}

// Function to handle OTP verification result
function handleOTPVerification(success, errorMessage = '') {
  const verificationStatusMsg = document.getElementById('email-verification-icon');
  verificationStatusMsg.style.display = 'block';
  verificationStatusMsg.style.color = success ? 'green' : 'red';
  verificationStatusMsg.innerHTML = success ? 'OTP Sent Successfully' : errorMessage;

  const sendOtpContainer = document.getElementById('sendOtpContainer');
  const verifyOtpContainer = document.getElementById('verifyOtpContainer');

  sendOtpContainer.style.display = success ? 'none' : 'block';
  verifyOtpContainer.style.display = success ? 'block' : 'none';

  if (!success) {
    document.getElementById('btn-sendOtp').innerHTML = 'Resend OTP';
    displayErrorMessage(errorMessage);
  }
}

// Helper function to display error/success messages
function displayErrorMessage(message) {
  const verificationStatusMsg = document.getElementById('email-verification-icon');
  verificationStatusMsg.style.display = 'block';
  verificationStatusMsg.style.color = 'red';
  verificationStatusMsg.innerHTML = message;

  document.getElementById('sendOtpContainer').style.display = 'block';
  document.getElementById('btn-sendOtp').innerHTML = 'Resend OTP';
  document.getElementById('verifyOtpContainer').style.display = 'none';
}

function displaySuccessMessage(message) {
  const verificationStatusMsg = document.getElementById('email-verification-icon');
  verificationStatusMsg.style.display = 'block';
  verificationStatusMsg.style.color = 'green';
  verificationStatusMsg.innerHTML = message;

  const sendOtpContainer = document.getElementById('sendOtpContainer');
  const verifyOtpContainer = document.getElementById('verifyOtpContainer');

  sendOtpContainer.style.display = 'none';
  verifyOtpContainer.style.display = 'none';
}


// function sendOTP() {
//     const email = document.getElementById('email').value;
  
//     // Make a fetch request to send OTP
//     fetch('/send_otp', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ email: email }),
//     })
//     .then(response => response.json())
//     .then(data => {
//       if (data.status) {
//         console.log(data.message);
  
//         // Hide email input and show OTP fields
//         document.getElementById('sendOtpContainer').style.display = 'none';
//         document.getElementById('verifyOtpContainer').style.display = 'block';
  
//         // Focus on the first OTP input field for better user experience
//         document.getElementById('otp').focus();
//       } else {
//         console.warn(data.error);
//         document.getElementById('sendOtpContainer').style.display = 'block';
//         document.getElementById('btn-sendOtp').innerHTML = 'Resend OTP';
//         displayErrorMessage(data.error);
//       }
//     })
//     .catch(error => {
//       console.error('Error sending OTP:', error);
//       displayErrorMessage('Failed to send OTP. Please try again.');
//     });
//   }
  
//   function verifyOTP() {
//     const enteredOTP = document.getElementById('otp').value;
  
//     // Make a fetch request to verify OTP
//     fetch('/verify_otp', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ otp: enteredOTP }),
//     })
//     .then(response => response.json())
//     .then(data => {
//       if (data.status) {
//         console.log(data.message);
//         displaySuccessMessage('Verified');
//         // Proceed with further actions after successful verification
//       } else {
//         console.warn(data.error);
//         displayErrorMessage(data.error);
//       }
//     })
//     .catch(error => {
//       console.error('Error verifying OTP:', error);
//       displayErrorMessage('Failed to verify OTP. Please try again.');
//     });
//   }
  
//   // Helper function to display error/success messages
//   function displayErrorMessage(message) {
//     const verificationStatusMsg = document.getElementById('email-verification-icon');
//     verificationStatusMsg.style.display = 'block';
//     verificationStatusMsg.style.color = 'red';
//     verificationStatusMsg.innerHTML = message;

//     document.getElementById('sendOtpContainer').style.display = 'block';
//     document.getElementById('btn-sendOtp').innerHTML = 'Resend OTP';

//     document.getElementById('verifyOtpContainer').style.display = 'none';

//   }
  
//   function displaySuccessMessage(message) {
//     const verificationStatusMsg = document.getElementById('email-verification-icon');
//     verificationStatusMsg.style.display = 'block';
//     verificationStatusMsg.style.color = 'green';
//     verificationStatusMsg.innerHTML = message;

//     const sendOtpContainer = document.getElementById('sendOtpContainer');
//     const otpContainer = document.getElementById('verifyOtpContainer');
//     sendOtpContainer.style.display = 'none'
//     otpContainer.style.display = 'none'
//   }
  
