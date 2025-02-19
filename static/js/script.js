// static/js/script.js
$(document).ready(function() {
    function loadFoods(type) {
        $.ajax({
            url: "/foods/filter-foods/", // URL مربوط به ویو filter_foods
            data: {
                'type': type
            },
            success: function(data) {
                $('#food-list').empty(); // پاک کردن محتوای قبلی
                data.forEach(function(food) {
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
            error: function(xhr, status, error) {
                console.error("Error fetching data:", error); // نمایش خطا در کنسول
            }
        });
    }

    // رویداد کلیک برای دکمه‌ها
    $('#all').click(function() {
        loadFoods('all');
    });

    $('#sandwiches').click(function() {
        loadFoods('sandwiches');
    });

    $('#pizzas').click(function() {
        loadFoods('pizzas');
    });

    // بارگذاری همه غذاها به صورت پیش‌فرض
    loadFoods('all');
});