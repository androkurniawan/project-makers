$(function(){
    $(document).scroll(function(){ 
        var $nav = $(".navbar");
        if ($(this).scrollTop() > $nav.height()) {
            $nav.addClass("scrolled");
            $nav.removeClass("navbar-dark");
            $nav.addClass("navbar-light");
        } else {
            $nav.removeClass("scrolled");
            $nav.addClass("navbar-dark");
            $nav.removeClass("navbar-light");
        }
    });
})

function getCookie(){
    let cookies = document.cookie
    let x = cookies.split("=")
    let y = x[1]

    if(y != null) {
        window.location.href = "home.html"
    }			
}

// Check Cookie Function to check the user has been login or not before now
function getCookie(){
    let cookies = document.cookie
    let x = cookies.split("=")
    let y = x[1]
    if(y == null) {
        window.location.href = "index.html"
    } else {
        customerOrHotel();
    }
}
    
function customerOrHotel() {
    let token = document.cookie;
    let splitToken = token.split(".");
    let user = JSON.parse(atob(splitToken[1]));
    let usernames = user["user"];
    let passwords = user["passkey"];

    if (usernames.length !== 0){   
        let usernameOrEmail = usernames;
        let password = passwords;

        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Basic " + btoa(usernameOrEmail + ":" + password));

        var raw = "";

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow',
        };
        
        fetch("http://127.0.0.1:5000/login", requestOptions)
            .then((response) => response.json())
            .then((result) => {
            if (result.message === "success" && result.user === "customer") {
                window.location.href = "home-customer.html";
            } else if (result.message === "success" && result.user === "hotel"){
                window.location.href = "home-hotel.html"
            }
            })
            .catch((error) => console.log(error));
    } else {
        window.location.href = "index.html"
    }
}

// Logout
function setCookie(cName, cValue, expDays) {
    let date = new Date();
    date.setTime(date.getTime() + expDays * 24 * 60 * 60 * 1000);
    const expires = "expires=" + date.toUTCString();
    document.cookie =
        cName + "=" + cValue + "; " + expires + "; path=/; SameSite=None; secure";
}

function logout() {
    if (confirm("Do you want to Logout?")) {
        setCookie("username", "", -1);
        location.href="index.html";
        console.log("BERHASIL LOGOUT");
    } else {
        console.log("CANCELED.")
    }
}