// report handler function
function toggle(){
    // To add blur effect to the background
    var blur = document.getElementById('to-blur');
    blur.classList.toggle('active');

    // Hide & active the popup window
    var popup = document.getElementById('report');
    popup.classList.toggle('active');
}

// send Email function
function sendEmail(){
    params = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        descbug: document.getElementById("descbug").value,
    }

    const serviceID = "service_g3ljxmr";
    const templateID = "template_ha6so86";

    emailjs.send(serviceID, templateID, params)
    .then((res) => {
        document.getElementById('name').value = "";
        document.getElementById('email').value = "";
        document.getElementById('descbug').value = "";
        console.log(res);
        alert('Email sent! Thanks.');
    })
    .catch((err) => console.log(err));
}