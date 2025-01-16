// // Handle form submission
// document.getElementById('requisitionForm').addEventListener('submit', async function (e) {
//   e.preventDefault(); // Prevent default form submission

//   if (validateForm()) {
//     try {
//       const formData = new FormData(this);
//       const response = await fetch(this.action, {
//         method: this.method,
//         body: formData,
//       });

//       const result = await response.json();

//       if (response.ok && result.status === 'success') {
//         // Show success notification
//         const notification = document.createElement('div');
//         notification.className = 'alert success';
//         notification.textContent = result.message;
//         document.querySelector('.form-container').prepend(notification);

//         // Automatically hide the notification after 5 seconds
//         setTimeout(() => notification.remove(), 5000);

//         // Clear the form
//         this.reset();
//       } else if (result.status === 'duplicate') {
//         // Show duplicate submission notification
//         const notification = document.createElement('div');
//         notification.className = 'alert error';
//         notification.textContent = result.message;
//         document.querySelector('.form-container').prepend(notification);

//         // Automatically hide the notification after 5 seconds
//         setTimeout(() => notification.remove(), 5000);
//       } else {
//         alert(result.message || 'Failed to submit the form.');
//       }
//     } catch (error) {
//       alert('An error occurred while submitting the form. Please try again later.');
//       console.error(error);
//     }
//   }
// });




// --------------------Logic 1--------------------

// function validateForm() {
//     let isValid = true;
  
//     function showError(id, message) {
//       const errorField = document.getElementById(id + 'Error');
//       if (message) {
//         errorField.textContent = message;
//         isValid = false;
//       } else {
//         errorField.textContent = '';
//       }
//     }
  
//     // Validate email
//     const email = document.getElementById('email').value;
//     showError('email', email.includes('@') ? '' : 'Invalid email.');
  
//     // Validate mobile number
//     const mobile = document.getElementById('mobile').value;
//     showError('mobile', /^\d{10}$/.test(mobile) ? '' : 'Invalid mobile number.');
  
//     // Validate date fields
//     const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
//     const dob = document.getElementById('dob').value;
//     showError('dob', dateRegex.test(dob) ? '' : 'Invalid date format. Use YYYY-MM-DD.');
  
//     const rccDate = document.getElementById('date').value;
//     showError('date', dateRegex.test(rccDate) ? '' : 'Invalid date format. Use YYYY-MM-DD.');
  
//     return isValid;
//   }

  
// This function clears the form fields
// function clearForm() {
//   document.getElementById("requisitionForm").reset(); // Reset all fields in the form
// }




// -------------Logic 2-----------


//Validate form data

function validateForm(event) {
  event.preventDefault();
  let isValid = true;

  function showError(id, message) {
    const errorField = document.getElementById(id + 'Error');
    if (message) {
      errorField.textContent = message;
      isValid = false;
    } else {
      errorField.textContent = '';
    }
  }

  // Validate email
  const email = document.getElementById('email').value;
  showError('email', email.includes('@') ? '' : 'Invalid email.');

  // Validate mobile number
  const mobile = document.getElementById('mobile').value;
  showError('mobile', /^\d{10}$/.test(mobile) ? '' : 'Invalid mobile number.');

  // Validate date fields
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  const dob = document.getElementById('dob').value;
  showError('dob', dateRegex.test(dob) ? '' : 'Invalid date format. Use YYYY-MM-DD.');

  const rccDate = document.getElementById('date').value;
  showError('date', dateRegex.test(rccDate) ? '' : 'Invalid date format. Use YYYY-MM-DD.');
  
  if (isValid) {
    // Submit the form via AJAX (or allow normal submission if no AJAX is used)
    const form = document.getElementById("requisitionForm");
    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
    })
      .then((response) => {
        if (response.ok) {
          alert("Form submitted successfully!");
          form.reset(); // Clear the form after successful submission
        } else {
          alert("You have already submitted the Railway Requisition Form.");
        }
      })
      .catch((error) => console.error("Error submitting form:", error));
  }

  return false; // Prevent default form submission
}







  
//   if (isValid) {
//     // Trigger the success modal after form validation
//     $('#successModal').modal('show');
//     document.getElementById("requisitionForm").reset(); // Clear the form
// }

// return isValid;
// }

// // Listen for form submission and handle clearing the form after success
// document.addEventListener("DOMContentLoaded", function () {
//   if (window.location.pathname === "/") {
//       // Clear the form if a flash message is present (after successful submission)
//       const flashMessage = document.querySelector(".alert");
//       if (flashMessage) {
//           clearForm();  // Clear the form after successful submission
//       }
//   }
// });
