$(document).ready(function () {
    $('#likes').click(function () {
        console.log("like clicked!");
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/stream/like/', {category_id: catid}, function (data) {
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });
    $('#suggestion').keyup(function () {
        var query;
        query = $(this).val();
        $.get('/stream/suggest/', {suggestion: query}, function (data) {
            $('#cats').html(data);
        });
    });

    $('.stream-add').click(function () {
        var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var name = $(this).attr("data-name");
        var me = $(this)
        $.get('/stream/add/',
            {category_id: catid, url: url, name: name}, function (data) {
                $('#pages').html(data);
                me.hide();
            });
    });
});
