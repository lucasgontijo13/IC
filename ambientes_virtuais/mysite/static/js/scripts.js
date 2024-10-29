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



function openEditModal(id, acao) {
    document.getElementById('editId').value = id;
    document.getElementById('editAcao').value = acao;
    var editModal = new bootstrap.Modal(document.getElementById('editModal'));
    editModal.show();
}

function saveEdit() {
    const id = document.getElementById('editId').value;
    const newAcao = document.getElementById('editAcao').value;

    // Atualiza o valor do select correspondente na tabela
    const select = document.querySelector(`select[name="action_${id}"]`);
    if (select) {
        select.value = newAcao;
    }

    // Adiciona o campo hidden de ID para garantir que o item_id seja enviado
    const editIdInput = document.createElement('input');
    editIdInput.type = 'hidden';
    editIdInput.name = 'editId';  // Nome correto para pegar no POST
    editIdInput.value = id;
    document.getElementById('mainForm').appendChild(editIdInput);

    // Configura o campo 'save' para 'temporary' para salvar no TemporaryActionModel
    const saveButton = document.createElement('input');
    saveButton.type = 'hidden';
    saveButton.name = 'save';
    saveButton.value = 'temporary';
    document.getElementById('mainForm').appendChild(saveButton);

    // Submete o formulário para salvar as alterações
    document.getElementById('mainForm').submit();
}




$(document).ready(function() {
    $('#carregarButton').click(function() {
        var selectedDate = $('#dateSelect').val();
        if (selectedDate) {
            $.ajax({
                type: "POST",
                url: "{% url 'index' %}",  // Certifique-se de que a URL está correta
                data: {
                    'selected_date': selectedDate,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function(response) {
                    $('#grafico_pizza').html(response.grafico_pizza);
                }
            });
        } else {
            alert("Por favor, selecione uma data.");
        }
    });
});