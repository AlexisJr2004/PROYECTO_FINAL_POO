// Variable de objetos
let d = document, c = console.log
// ------------------- carga inicial de la pagina ------------------------
d.addEventListener('DOMContentLoaded', function (e) {
    // Declaracion de variables
    let $customer = d.getElementById("id_customer")
    let $payment_method = d.getElementById("id_payment_method")
    $customer.selectedIndex = 1
    $payment_method.selectedIndex = 1
    let $detailBody = d.getElementById('detalle')
    let $product = d.getElementById('product')
    let $btnAdd = d.getElementById("btnAdd")
    c($btnAdd)
    let $btnGrabar = d.getElementById("btnGrabar")
    let $form = d.getElementById("frmSale")
    let detailSale = []
    let sub = 0
    //alert("entro al dom JS")
    console.log("detalle= ", detail_sales)
    if (detail_sales.length > 0) {
        detailSale = detail_sales.map(item => {
            let { product: id, product__description: description, quantity: quantify, price, subtotal: sub, iva } = item
            price = parseFloat(price)
            quantify = parseInt(quantify)
            iva = parseFloat(iva)
            sub = parseFloat(sub)
            return { id, description, price, quantify, iva, sub }
            //[{id:1...},{id:2...}]
        })
        present()
        totals()
    }
    // Declaracion de metodos
    // ---------- calcula el total del producto y lo añade al arreglo detailSale[] ----------
    const calculation = (id, description, iva, price, quantify) => {
        // debugger;
        const product = detailSale.find(prod => prod.id == id)
        if (product) {
            if (!confirm(`¿Ya existe ingresado ${product.description} =>  Desea actualizarlo?`)) return
            quantify += product.quantify
            detailSale = detailSale.filter(prod => prod.id !== id)
        }
        iva = iva > 0 ? ((price * quantify) * (iva / 100)).toFixed(2) : "0"
        iva = parseFloat(iva)
        sub = (price * quantify + iva).toFixed(2)
        sub = parseFloat(sub)
        detailSale.push({ id, description, price, quantify, iva, sub })
        present()
        totals()
    }

    const productChange = (e) => {
        c("entro al changeproduct")
        const selectedOption = e.target.selectedOptions[0];
        const price = selectedOption.getAttribute('data-price');
        d.getElementById('price').value = price
        // reCalculation(id)
    };
    $product.addEventListener('change', productChange);
    // llama la primera vez al inicializar el select product
    productChange({ target: $product });
    // ---------------  borra el producto dado el id en el arreglo detailSale[] ------------
    const deleteproduct = (id) => {
        detailSale = detailSale.filter((item) => item.id !== id)
        present()
        totals()
    }
    // recorre el arreglo detailSale y renderiza el detalle del producto -----------
    function present() {
        c("estoy en present()")
        let detalle = d.getElementById('detalle')
        detalle.innerHTML = ""
        detailSale.forEach((product) => {
            detalle.innerHTML += `<tr class=dark:text-gray-400 bg-white border-b dark:bg-[#0b1121] dark:border-secundario hover:bg-gray-50 dark:hover:bg-[#121c33]>
            <td>${product.id}</td>
            <td>${product.description}</td>
            <td>${product.price}</td>
            <td>${product.quantify}</td>
            <td>${product.iva}</td>
            <td>${product.sub}</td>
            <td class="text-center ">
                <button rel="rel-delete" data-id="${product.id}" class="text-red-600 dark:text-red-500"><i class="fa-solid fa-trash"></i></button>
            </td>
          </tr>`
        });
    }
    // ----- Sumariza del arreglo detailSale[] y lo renderiza en la tabla de la pagina -----
    function totals() {
        const result = detailSale.reduce((acc, product) => {
            acc.iva += product.iva;
            acc.sub += product.sub;
            return acc;
        }, { iva: 0, sub: 0 });
        d.getElementById('id_subtotal').value = (result.sub - result.iva).toFixed(2)
        d.getElementById('id_iva').value = result.iva.toFixed(2)
        d.getElementById('id_total').value = (result.sub).toFixed(2)
    }
    // metodo asincrono grabar venta
    async function saveSale(urlPost, urlSuccess) {
        const formData = new FormData($form);
        formData.append("detail", JSON.stringify(detailSale));

        let csrf = d.querySelector('[name=csrfmiddlewaretoken]').value;

        // Mostrar los datos de FormData en la consola
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
            c(res)
            if (!res.ok) {
                const text = await res.text();
                c("error=> " + text)
                throw new Error(`HTTP error! Status: ${res.status}, Response: ${text}`);
            }

            const post = await res.json();
            console.log("Server message:", post.msg); // Mostrar el mensaje en la consola
            alert(post.msg);
            window.location.href = urlSuccess;
        } catch (error) {
            console.error("Fetch error:", error);
            alert("Fetch error: " + error);
        }
    }

    // // fin de grabar 
    // ------------- manejo del DOM -------------
    // ---------- envia los datos de la venta con su detalle al backend por ajax para grabarlo ----------
    $form.addEventListener('submit', async (e) => {
        e.preventDefault()
        if (parseFloat(d.getElementById('id_total').value) > 0.00) {
            await saveSale(save_url, '/sale/sales_list/')
        } else {
            alert("!!!Faltan datos de productos para grabar la venta!!!")
        }
    });

    $btnAdd.addEventListener('click', (e) => {
        debugger;
        let quantify = parseInt(d.getElementById('quantify').value)
        let stock = parseInt($product.options[$product.selectedIndex].dataset.stock);
        c(quantify)
        if (quantify > 0 && quantify <= stock) {
            let idProd = parseInt($product.value)
            let price = d.getElementById('price').value
            price = parseFloat(price.replace(',', '.'))
            let iva = $product.options[$product.selectedIndex].dataset.iva;
            iva = parseFloat(iva.replace(',', '.'))
            let description = $product.options[$product.selectedIndex].text
            calculation(idProd, description, iva, price, quantify)
            // d.getElementById('id_nume_hours').value = ""
        } else {
            alert(`cantidad negativa o superior al stock:[${stock}]`)
        }
    });

    $detailBody.addEventListener('click', (e) => {
        const fil = e.target.closest('button[rel=rel-delete]')
        c(fil)
        if (fil) deleteproduct(parseInt(fil.getAttribute('data-id')))
    });

    const paymentInput = d.getElementById('id_payment');
    const totalInput = d.getElementById('id_total');
    const changeInput = d.getElementById('id_change');

    function updateChange() {
        const payment = parseFloat(paymentInput.value) || 0;
        const total = parseFloat(totalInput.value) || 0;
        const change = payment - total;
        
        if (!isNaN(change)) {
            changeInput.value = change.toFixed(2);
        } else {
            changeInput.value = '0.00';
        }
    }

    if (paymentInput && totalInput && changeInput) {
        paymentInput.addEventListener('input', updateChange);
        totalInput.addEventListener('input', updateChange);
        // Calcular cambio inicial
        updateChange();
    } else {
        c('No se encontraron uno o más campos necesarios');
    }
});