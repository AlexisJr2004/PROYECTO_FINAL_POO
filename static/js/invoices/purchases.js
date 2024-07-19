let d = document, c = console.log;
d.addEventListener('DOMContentLoaded', function (e) {
    // Declaracion de variables
    let $supplier = d.getElementById("id_supplier");
    let $issue_date = d.getElementById("id_issue_date");
    let $num_document = d.getElementById("id_num_document");
    let $subtotal = d.getElementById("id_subtotal");
    let $iva = d.getElementById("id_iva_purchase");
    let $total = d.getElementById("id_total");
    let $detailBody = d.getElementById('detalle');
    let $product = d.getElementById('product');
    let $btnAdd = d.getElementById("btnAdd");
    let $form = d.getElementById("frmPurchase");
    let detailPurchase = [];
    let sub = 0;

    // Carga inicial de detalles de compra si existen
    console.log("detalle= ", detail_purchases)
    if (detail_purchases.length > 0) {
        detailPurchase = detail_purchases.map(item => {
            let { product, product__description: description, quantify, cost, subtotal, iva } = item;
            return {
                id: product,
                description,
                cost: parseFloat(cost),
                stock: parseFloat(quantify),  // Cambiado de 'stock' a 'quantify'
                subtotal: parseFloat(subtotal),
                iva: parseFloat(iva)
            };
        });
        present();
        totals();
    }
    // Declaracion de metodos
    // Calcula el total del producto y lo añade al arreglo detailPurchase[]
    const calculation = (id, description, cost, stock) => {
        const product = detailPurchase.find(prod => prod.id == id);
        if (product) {
            if (!confirm(`¿Ya existe ingresado ${product.description} =>  Desea actualizarlo?`)) return;
            stock += product.stock;
            detailPurchase = detailPurchase.filter(prod => prod.id !== id);
        }
        c(`Datos recibidos de calculation: id= ${id}, description= ${description}, cost= ${cost}, stock= ${stock}`);
        cost = parseFloat(cost);  // Asegurar que cost sea tratado como decimal
        const subtotal = (cost * stock).toFixed(2);
        let iva = $product.options[$product.selectedIndex].dataset.iva;
        iva = parseFloat(iva.replace(',', '.'));
        iva = ((parseFloat(subtotal) * iva) / 100).toFixed(2);
        detailPurchase.push({ id, description, cost, stock, subtotal, iva });
        present();
        totals();
    };

    // Cambio de producto seleccionado; Mostrar costo y stock del producto
    const productChange = (e) => {
        c("entro al changeproduct");
        const selectedOption = e.target.selectedOptions[0];
        const cost = selectedOption.getAttribute('data-cost');
        const stock = selectedOption.getAttribute('data-stock');
        if (cost && stock) {
            d.getElementById('cost').value = cost;
            d.getElementById('stock').value = stock;
            c(`cost= ${cost}, stock= ${stock}`);
        } else {
            d.getElementById('cost').value = '';
            d.getElementById('stock').value = '';
        }
    };
    
    $product.addEventListener('change', productChange);
    
    // Llamada inicial al cambio de producto
    if ($product.value) {
        productChange({ target: $product });
    }

    // Elimina un producto del detalle de compra
    const deleteProduct = (id) => {
        detailPurchase = detailPurchase.filter(item => item.id !== id);
        present();
        totals();
    };

    // Renderiza el detalle de compra en la tabla
    function present() {
        let detalle = d.getElementById('detalle');
        detalle.innerHTML = "";
        detailPurchase.forEach((product) => {
            detalle.innerHTML += `<tr class=dark:text-gray-400 bg-white border-b dark:bg-[#0b1121] dark:border-secundario hover:bg-gray-50 dark:hover:bg-[#121c33]>
                <td>${product.id}</td>
                <td>${product.description}</td>
                <td>${product.cost}</td>
                <td>${product.stock}</td>
                <td>${product.subtotal}</td>
                <td>${product.iva}</td>
                <td><button rel="rel-delete" data-id="${product.id}" class="text-red-600" onclick="deleteProduct(${product.id})"><i class="fa-solid fa-trash"></i></button></td>
            </tr>`;
        });
    }

    // Calcula totales de la compra
    function totals() {
        const result = detailPurchase.reduce((acc, product) => {
            acc.subtotal += parseFloat(product.subtotal);
            acc.iva += parseFloat(product.iva);
            return acc;
        }, { subtotal: 0, iva: 0 });
        $subtotal.value = result.subtotal.toFixed(2);
        $iva.value = result.iva.toFixed(2);
        $total.value = (result.subtotal + result.iva).toFixed(2);
    }

    // Método asincrónico para guardar la compra
    async function savePurchase(urlPost, urlSuccess) {
        const formData = new FormData($form);
        formData.append("detail", JSON.stringify(detailPurchase));

        let csrf = d.querySelector('[name=csrfmiddlewaretoken]').value;

        console.log('FormData antes de enviar:');
        c(`csrf=${csrf}`)
        for (let [name, value] of formData.entries()) {
            console.log(`${name}: ${value}`);
        }

        try {
            const res = await fetch(urlPost, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrf,
                },
                body: formData
            });
            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }
            const post = await res.json();
            alert(post.msg);
            window.location.href = urlSuccess;
        } catch (error) {
            console.error("Fetch error:", error);
            alert("Fetch error: " + error);
        }
    }

    // Envía los datos de la compra al backend para guardarla
    $form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (parseFloat($total.value) > 0.00) {
            await savePurchase(save_url, '/purchase/purchases_list/');
        } else {
            alert("Faltan datos de productos para grabar la compra.");
        }
    });

    // Agrega un producto al detalle de la compra
    $btnAdd.addEventListener('click', (e) => {
        let stock = parseInt(d.getElementById('stock').value);
        let idProd = parseInt($product.value);
        let cost = d.getElementById('cost').value;
        cost = cost.replace(',', '.');  // Aquí corregimos para asignar el valor modificado a 'cost'
        cost = parseFloat(cost);
        let description = $product.options[$product.selectedIndex].text;
        c(`Datos a enviar: stock= ${stock}, idProd= ${idProd}, cost= ${cost}, description= ${description}`);
        calculation(idProd, description, cost, stock);
    });    

    // Elimina un producto del detalle de compra
    $detailBody.addEventListener('click', (e) => {
        const fil = e.target.closest('button[rel=rel-delete]');
        if (fil) {
            deleteProduct(parseInt(fil.getAttribute('data-id')));
        }
    });
});