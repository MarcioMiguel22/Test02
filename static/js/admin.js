/**
 * Funções JavaScript para o Painel Administrativo
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicializa popovers do Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Adiciona confirmação para ações de exclusão
    setupDeleteConfirmation();
});

/**
 * Configura confirmação para ações de exclusão
 */
function setupDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.delete-button, .deletelink');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.')) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Mostra uma mensagem de notificação
 * @param {string} message - A mensagem a ser exibida
 * @param {string} type - O tipo da mensagem (success, danger, warning, info)
 */
function showNotification(message, type = 'info') {
    const container = document.createElement('div');
    container.className = `alert alert-${type} alert-dismissible fade show notification`;
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '9999';
    container.style.maxWidth = '300px';
    
    container.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(container);
    
    // Remove a notificação após 5 segundos
    setTimeout(() => {
        container.classList.remove('show');
        setTimeout(() => {
            container.remove();
        }, 300);
    }, 5000);
}
