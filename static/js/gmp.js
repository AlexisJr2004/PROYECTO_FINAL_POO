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
                            <div class="bg-gray-200 dark:bg-principal p-2 m-2 rounded-3xl">
                                <div class="flex flex-wrap items-center justify-center text-center space-x-2">
                                    <h2 class="text-lg dark:text-blue-300 mb-0 font-Pacifico flex items-center">
                                        <i class="${module.module_icon} mr-2"></i>${module.module_name}
                                    </h2>
                                    <button type="button" class="select-all-btn text-blue-300 hover:text-blue-500 rounded-full p-0">
                                        <i class="ri-checkbox-blank-fill text-2xl"></i>
                                    </button>
                                </div>
                                <div class="grid items-center permissions-group">
                                    ${module.permissions.map(perm => `
                                        <label class="inline-flex items-center mr-4 mb-2">
                                            <input type="checkbox" name="permissions[]" value="${perm.id}" 
                                                ${perm.selected ? 'checked' : ''} class="checkbox-container shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-[10px] p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light">
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
                        button.addEventListener('click', function () {
                            const checkboxes = this.parentElement.nextElementSibling.querySelectorAll('input[type="checkbox"]');
                            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
                            checkboxes.forEach(cb => cb.checked = !allChecked);
                            this.innerHTML = allChecked ? '<i class="ri-checkbox-blank-fill text-2xl"></i>' : '<i class="ri-checkbox-fill text-2xl"></i>';
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