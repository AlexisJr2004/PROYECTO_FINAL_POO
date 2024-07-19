document.addEventListener('DOMContentLoaded', function() {
    const groupSelect = document.querySelector('#id_group');
    const permissionsList = document.querySelector('#permissions-list');

    groupSelect.addEventListener('change', function() {
        const groupId = this.value;
        if (groupId) {
            fetch(`?group_id=${groupId}`)
                .then(response => response.json())
                .then(data => {
                    permissionsList.innerHTML = '';
                    data.permissions_data.forEach(module => {
                        const moduleDiv = document.createElement('div');
                        moduleDiv.className = 'module-container mb-4';
                        moduleDiv.innerHTML = `
                            <div class="bg-gray-200 dark:bg-[#0A0E21] p-2 m-2 rounded-3xl">
                                <h3 class="text-lg dark:text-blue-300 font-semibold mb-2">${module.module_name}</h3>
                                <button type="button" class="select-all-btn bg-blue-700 hover:bg-blue-800 text-white py-2 px-4 rounded-full mb-2">
                                    Seleccionar todos
                                </button>
                                <div class="grid items-center permissions-group">
                                    ${module.permissions.map(perm => `
                                        <label class="inline-flex items-center mr-4 mb-2">
                                            <input type="checkbox" name="permissions[]" value="${perm.id}" 
                                                ${perm.selected ? 'checked' : ''} class="checkbox-container">
                                            <span class="ml-2 dark:text-gray-400">${perm.name}</span>
                                        </label>
                                    `).join('')}
                                </div>
                            </div>
                        `;
                        permissionsList.appendChild(moduleDiv);
                    });

                    // Agregar event listeners para los botones "Seleccionar todos"
                    document.querySelectorAll('.select-all-btn').forEach(button => {
                        button.addEventListener('click', function() {
                            const checkboxes = this.nextElementSibling.querySelectorAll('input[type="checkbox"]');
                            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
                            checkboxes.forEach(cb => cb.checked = !allChecked);
                            this.textContent = allChecked ? 'Seleccionar todos' : 'Deseleccionar todos';
                        });
                    });
                });
        } else {
            permissionsList.innerHTML = '';
        }
    });

    const form = document.querySelector('#group-module-permission-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert('Error al guardar GMP');
            }
        });
    });
});