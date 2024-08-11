/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

document.addEventListener('DOMContentLoaded', function() {
    const fileUpload = document.getElementById('file-upload');
    const fileName = document.getElementById('file-name');

    fileUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = 'Selecione um ficheiro';
        }
    });

    // Ensure the file name text is reset on page load
    fileName.textContent = 'Selecione um ficheiro';
});
document.getElementById('file-upload').addEventListener('change', function() {
    // Se você não quiser que o formulário seja enviado automaticamente, não adicione código aqui
    // Se houver código para enviar automaticamente, remova ou ajuste conforme necessário
});


$(document).ready( function () {
    $('#datatablesSimple').DataTable();
});

document.getElementById('upload-form').addEventListener('submit', function(event) {
    var fileInput = document.getElementById('file-upload');
    if (!fileInput.files.length) {
        event.preventDefault(); // Impede o envio do formulário
        alert('Selecione um arquivo para enviar');
    }
});




