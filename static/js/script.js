// static/js/script.js
$(document).ready(function () {
    function loadFoods(type) {
        $.ajax({
            url: "/foods/filter-foods/", // URL مربوط به ویو filter_foods
            data: {
                'type': type
            },
            success: function (data) {
                $('#food-list').empty(); // پاک کردن محتوای قبلی
                data.forEach(function (food) {
                    // اضافه کردن غذاها به صفحه
                    $('#food-list').append(
                        '<div class="food-item">' +
                        '<a href="' + food.url + '">' + // لینک به صفحه جزئیات
                        '<img src="' + food.image + '" alt="' + food.title + '">' + // نمایش عکس
                        '<h3>' + food.title + '</h3>' + // نمایش عنوان
                        '<p>' + food.price + ' T</p>' + // نمایش قیمت
                        '</a>' +
                        '</div>'
                    );
                });
            },
            error: function (xhr, status, error) {
                console.error("Error fetching data:", error); // نمایش خطا در کنسول
            }
        });
    }

    // رویداد کلیک برای دکمه‌ها
    $('#all').click(function () {
        loadFoods('all');
    });

    $('#sandwiches').click(function () {
        loadFoods('sandwiches');
    });

    $('#pizzas').click(function () {
        loadFoods('pizzas');
    });

    // بارگذاری همه غذاها به صورت پیش‌فرض
    loadFoods('all');
});

$(document).ready(function () {
    // وقتی فرم جستجو submit شد
    $('#search-form').on('submit', function (e) {
        e.preventDefault(); // جلوگیری از ارسال سنتی فرم

        var query = $('#search-input').val(); // گرفتن مقدار وارد شده توسط کاربر
        console.log('Search query:', query); // نمایش کوئری در کنسول (برای دیباگ)

        // ارسال درخواست AJAX
        $.ajax({
            url: "/foods/search/", // آدرس view ای که جستجو رو انجام می‌ده
            type: 'GET',
            data: {
                'q': query
            },
            success: function (response) {
                console.log('Search results:', response); // نمایش نتایج در کنسول (برای دیباگ)
                displayResults(response.results); // نمایش نتایج
            },
            error: function (xhr, status, error) {
                console.error('AJAX error:', error); // نمایش خطا در کنسول (برای دیباگ)
            }
        });
    });

    // تابع برای نمایش نتایج جستجو
    function displayResults(results) {
        var resultsHtml = '';

        if (results.length > 0) {
            resultsHtml += '<ul>';
            results.forEach(function (result) {
                resultsHtml += '<li>';
                resultsHtml += '<strong>' + result.type + ':</strong> ' + result.title; // نمایش نوع و نام نتیجه
                resultsHtml += '</li>';
            });
            resultsHtml += '</ul>';
        } else {
            resultsHtml = '<p>No results found.</p>';
        }

        $('#search-results').html(resultsHtml); // نمایش نتایج در div مربوطه
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Event listeners for plus and minus buttons
    document.querySelectorAll('.quantity-plus, .quantity-minus').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const productId = this.getAttribute('data-product-id');
            const modelName = this.getAttribute('data-model-name');

            // 🟢 لاگ بگیر برای چک کردن مقدار‌ها
            console.log("Product Id:", productId);
            console.log("Model Name:", modelName);

            if (!productId || !modelName) {
                console.error("Missing productId or modelName!");
                return;
            }

            const action = this.classList.contains('quantity-plus') ? 'increase' : 'decrease';
            updateCart(productId, modelName, action);
        });
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to send AJAX request and update the cart
function updateCart(productId, modelName, action) {
    console.log(`Fetching URL: /cart/update/${modelName}/${productId}/`);  // لاگ مسیر

    fetch(`/cart/update/${modelName}/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ action: action })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // به‌روزرسانی مقدار تعداد محصول در صفحه
            const quantityInput = document.querySelector(`.qty-input[data-product-id="${productId}"]`);
            if (quantityInput) {
                quantityInput.value = data.new_quantity;
            }

            // به‌روزرسانی مجموع قیمت هر محصول
            updateTotalPrice(productId, data.new_quantity, data.price);

            // به‌روزرسانی تعداد کل محصولات در سبد خرید
            updateCartTotalQuantity(data.cart);

            // به‌روزرسانی مجموع کل قیمت سبد خرید
            updateCartTotalPrice(data.cart);

            // به‌روزرسانی قیمت نهایی (order_total)
            updateOrderTotal(data.order_total);
        }
    })
    .catch(error => console.error("Error in fetch:", error));
}

// تابع برای به‌روزرسانی مجموع قیمت هر محصول
function updateTotalPrice(productId, newQuantity, price) {
    const totalPriceElement = document.querySelector(`.total-price[data-product-id="${productId}"]`);
    if (totalPriceElement) {
        const totalPrice = newQuantity * price;
        totalPriceElement.textContent = `${totalPrice.toLocaleString()} T`;  // اضافه کردن کاما
    }
}

// تابع برای به‌روزرسانی تعداد کل محصولات در سبد خرید
function updateCartTotalQuantity(cart) {
    const totalQuantityElement = document.querySelector('.cart-total-quantity');
    if (totalQuantityElement) {
        let totalQuantity = 0;
        for (const key in cart) {
            totalQuantity += cart[key].quantity;
        }
        totalQuantityElement.textContent = totalQuantity;
    }
}

// تابع برای به‌روزرسانی مجموع کل قیمت سبد خرید
function updateCartTotalPrice(cart) {
    const totalPriceElement = document.querySelector('.cart-total-price');
    if (totalPriceElement) {
        let totalPrice = 0;
        for (const key in cart) {
            totalPrice += cart[key].quantity * cart[key].price;
        }
        totalPriceElement.textContent = `${totalPrice.toLocaleString()} T`;  // اضافه کردن کاما
    }
}

// تابع برای به‌روزرسانی قیمت نهایی (order_total)
function updateOrderTotal(orderTotal) {
    const orderTotalElement = document.querySelector('.order-total');
    if (orderTotalElement) {
        orderTotalElement.textContent = `${orderTotal.toLocaleString()} T`;  // اضافه کردن کاما
    }
}

$(document).ready(function() {
    $('.ajax-contact').on('submit', function(e) {
        e.preventDefault();  // جلوگیری از ارسال معمولی فرم
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),
            success: function(response) {
                // پردازش پاسخ JSON
                if (response.status === 'success') {
                    form.find('.form-messages').html('<div class="alert alert-success">' + response.message + '</div>');
                } else {
                    form.find('.form-messages').html('<div class="alert alert-danger">' + response.message + '</div>');
                }
            },
            error: function(xhr, status, error) {
                // نمایش خطا اگر مشکلی پیش اومد
                var errorMessage = 'خطا در ارسال پیام!';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                form.find('.form-messages').html('<div class="alert alert-danger">' + errorMessage + '</div>');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.quick-view').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            var modelName = this.getAttribute('data-model-name');
            var productId = this.getAttribute('data-product-id');

            fetch(`/foods/product/${modelName}/${productId}/`)
                .then(response => response.json())
                .then(data => {
                    // فرمت قیمت با کاما
                    data.price = new Intl.NumberFormat().format(data.price);

                    // پر کردن مودال با اطلاعات محصول
                    document.querySelector('#QuickView .product-title').textContent = data.title;
                    document.querySelector('#QuickView .price .current-price').textContent = `${data.price}`;
                    document.querySelector('#QuickView .text').textContent = data.description;
                    document.querySelector('#QuickView .img img').src = data.image_url;

                    // نمایش مودال
                    $.magnificPopup.open({
                        items: {
                            src: '#QuickView',
                            type: 'inline'
                        }
                    });
                })
                .catch(error => {
                    console.error('❌ AJAX Error:', error);
                    alert("There was an error loading the product details.");
                });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const sortingSelect = document.getElementById('sorting-select');

    if (sortingSelect) {
        sortingSelect.addEventListener('change', function () {
            const selectedValue = this.value;

            // ساخت URL با پارامتر مرتب‌سازی
            const url = new URL(window.location.href);
            url.searchParams.set('orderby', selectedValue);

            // ارسال درخواست AJAX
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(data => {
                    // استخراج بخش product-list از پاسخ سرور
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(data, 'text/html');
                    const newProductList = doc.getElementById('product-list');

                    if (newProductList) {
                        document.getElementById('product-list').innerHTML = newProductList.innerHTML;
                    } else {
                        console.error('New product list not found in response!');
                    }
                })
                .catch(error => {
                    console.error('Error during fetch:', error);
                });
        });
    } else {
        console.error('Sorting select element not found!');
    }
});