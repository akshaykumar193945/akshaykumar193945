
function sendOTP() {
    const email = document.getElementById('email').value;
    console.log('in sendOtp');
    console.log(email);
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
        verification_status_msg = document.getElementById('email-verification-icon') 
        if (data.status){
            console.log(data.message);
            document.getElementById('otpContainer').style.display = 'block';
        } else {
            console.warn(data.error);
            verification_status_msg.style.display = 'block';
            verification_status_msg.style.color = 'red';
            verification_status_msg.innerHTML = data.error;
        }
        // Display OTP input field
    })
    .catch(error => {
        console.error('Error sending OTP:', error);
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
        document.getElementById('btn-sendOtp').style.display = 'none'; 
        verification_status_msg = document.getElementById('email-verification-icon') 
        btnVerifyOTP = document.getElementById('btn-verifyOTP')
        otpContainer = document.getElementById('otpContainer') 
        
        if (data.status){
            console.log(data.message);
            verification_status_msg.innerHTML = '<p>Verified</p>';                
            verification_status_msg.style.display = 'block';                
            verification_status_msg.style.color = 'green'; 
            btnVerifyOTP.style.display = 'none'; 
            otpContainer.style.display = 'none';               

        } else {
            console.warn(data.error);
            verification_status_msg.innerHTML = '<p>Invalid OTP !</p>';                
            verification_status_msg.style.display = 'block';              
            verification_status_msg.style.color = 'red';                
            btnVerifyOTP.style.display = 'none';                
            otpContainer.style.display = 'none';   
            // document.getElementById('btn-sendOtp').style.display = 'block'; 
            // document.getElementById('btn-sendOtp').innerHTML = '<p>Re-Send</p>'; 

        }
    })
    .catch(error => {
        console.error('Error verifying OTP:', error);
    });
}