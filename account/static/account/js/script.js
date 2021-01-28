$('#following-btn').click(function () {

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken')

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
 return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});



let user_id = $('#following-btn').attr('data-id');
let follow = $('#following-btn').text()

if(follow == 'follow'){
    var url = '/account/follow/'
    var btnText = 'unfollow'
    var btnClass = 'btn btn-warning mb-3'
}else{
    var url = '/account/unfollow/'
    var btnText = 'follow'
    var btnClass = 'btn btn-primary mb-3'

}
    $.ajax({
        url: url,
        method: 'POST',
        data : {
            'user_id':user_id,
        },
        success:function (data) {
            if(data['status']==='ok'){
                $('#following-btn').text(btnText)
                $('#following-btn').attr({'class':btnClass})
            }
        }
    });
});