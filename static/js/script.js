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

$(document).ready(function() {
    // وقتی فرم جستجو submit شد
    $('#search-form').on('submit', function(e) {
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
            success: function(response) {
                console.log('Search results:', response); // نمایش نتایج در کنسول (برای دیباگ)
                displayResults(response.results); // نمایش نتایج
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', error); // نمایش خطا در کنسول (برای دیباگ)
            }
        });
    });

    // تابع برای نمایش نتایج جستجو
    function displayResults(results) {
        var resultsHtml = '';

        if (results.length > 0) {
            resultsHtml += '<ul>';
            results.forEach(function(result) {
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