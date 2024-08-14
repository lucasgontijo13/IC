window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple, {
            perPage: Number.MAX_VALUE, // Define o número máximo de linhas por página
            perPageSelect: false // Remove o seletor de número de itens por página
        });
    }
});