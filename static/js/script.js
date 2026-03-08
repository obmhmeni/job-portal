// Future mein search filter, popup etc add kar sakte hain
console.log("Job Portal Bihar Loaded");

if (window.name === 'logged_in') {  // From backend redirect
    const popup = document.getElementById('welcomePopup');
    popup.classList.remove('d-none');
    setTimeout(() => popup.classList.add('d-none'), 2000);
}
