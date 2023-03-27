// Operating login/register forms with AJAX
$(document).ready(function () {

    function showLoginForm() {
        $.ajax({
            url: '/login/',
            type: 'GET',
            success: function (response) {
                console.log('succes', response.text)
                const wrapper = document.querySelector('.wrapper');
                wrapper.classList.add('active-popup');
                wrapper.innerHTML = $(response).find('.wrapper').html();
                const iconClose = document.querySelector('.icon-close');
                iconClose.addEventListener('click', function () {
                    wrapper.classList.remove('active-popup');
                });

                const registerLink = document.querySelector('#register-link');
                registerLink.addEventListener('click', showRegisterForm);
                const form = document.querySelector('#login-form');
                form.addEventListener('submit', function (event) {
                    event.preventDefault();
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    $.ajax({
                        url: '/login/',
                        type: 'POST',
                        data: {
                            'username': $('input[name="username"]').val(),
                            'password': $('input[name="password"]').val(),
                            'csrfmiddlewaretoken': csrftoken
                        },
                        beforeSend: function (xhr) {
                            xhr.setRequestHeader('x-requested-with', 'XMLHttpRequest');
                        },
                        success: function (data) {
                            const message = $('.message');
                            if (data.success) {
                                window.location.href = data.url;
                            } else {
                                const error_msg = $('<span>').text("Username and password doesn't match");
                                message.append(error_msg);
                                message.css('display', 'flex');
                            }
                            const messageBtn = $('#message-button');
                            messageBtn.on('click', () => {
                                message.css('display', 'none');
                                message.find('span').remove();
                            });
                        },
                    });
                });
            },
        });
    }

    function showRegisterForm() {
        $.ajax({
            url: '/register/',
            type: 'GET',
            success: function (response) {
                const wrapper = document.querySelector('.wrapper');
                wrapper.classList.add('active-popup', 'active');
                wrapper.innerHTML = $(response).find('.wrapper').html();
                const iconClose = document.querySelector('.icon-close');
                iconClose.addEventListener('click', function () {
                    wrapper.classList.remove('active-popup', 'active');
                });
                const loginLink = document.querySelector('.login-link');
                loginLink.addEventListener('click', function () {
                    wrapper.classList.remove('active')
                    showLoginForm()
                });
                const form = document.querySelector('#register-form');
                form.addEventListener('submit', function (event) {
                    event.preventDefault();
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    $.ajax({
                        url: '/register/',
                        type: 'POST',
                        data: {
                            'email': $('input[name="email"]').val(),
                            'username': $('input[name="username"]').val(),
                            'password': $('input[name="password"]').val(),
                            'password_confirmation': $('input[name="password_confirmation"]').val(),
                            'join_clan': $('input[name="join_clan"]').prop('checked'),
                            'csrfmiddlewaretoken': csrftoken
                        },
                        beforeSend: function (xhr) {
                            xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
                        },
                        success: function (data) {
                            const message = $('.message');
                            if (data.success) {
                                const successMsg = $('<span>').text('Registration successful!');
                                message.append(successMsg);
                                message.css('display', 'flex');
                            } else {
                                const error_msg = $('<span>').text('Error: ');
                                for (const messages of Object.values(data.errors)) {
                                    error_msg.append($('<div>').text(messages.join(', ')));
                                }
                                message.append(error_msg);
                                message.css('display', 'flex');
                            }
                                const messageBtn = $('#message-button');
                                messageBtn.on('click', () => {
                                    message.css('display', 'none');
                                    message.find('span').remove();
                                    window.location.href = ''
                                });
                        },
                    });
                });
            },
        });
    }

    $('.btnLogin-popup').click(showLoginForm);

});


const links = document.querySelectorAll('.menu-link');
links.forEach(link => {
    link.addEventListener('mouseover', () => {
        link.style.color = 'Orange';
    });

    link.addEventListener('mouseout', () => {
        link.style.color = 'Black';
    });
});
