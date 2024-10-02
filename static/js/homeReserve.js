const profileCards = document.querySelectorAll('.card'); // Selecciona todas las tarjetas

profileCards.forEach((profileCard, index) => {
    const arrowIcon = profileCard.querySelector('.arrow-icon');
    const profileMenu = profileCard.querySelector('.profile-menu');

    profileCard.addEventListener('mouseenter', () => {
        // Muestra el ícono de flecha cuando el mouse entra en la tarjeta
        arrowIcon.style.left = '0';
        setTimeout(() => {
            arrowIcon.style.opacity = '1';
        }, 0);
    });

    profileCard.addEventListener('mouseleave', () => {
        // Oculta el ícono de flecha y el menú cuando el mouse sale de la tarjeta
        arrowIcon.style.left = '0';
        arrowIcon.style.opacity = '0';
        profileMenu.style.opacity = '0'; // También oculta el menú
    });

    arrowIcon.addEventListener('click', (e) => {
        e.stopPropagation();

        // Alternar la visibilidad del menú emergente
        if (profileMenu.style.opacity === '1') {
            profileMenu.style.opacity = '0';
        } else {
            profileMenu.style.opacity = '1';

        }
    });

    document.addEventListener('click', (e) => {
        if (profileMenu.style.opacity === '1' && e.target !== arrowIcon) {
            profileMenu.style.opacity = '0';
        }
    });

    profileMenu.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});


$(document).ready(function () {
    $('.stars i').hover(function () {
        var value = $(this).data('value');
        highlightStars(value);
    });

    $('.stars').mouseleave(function () {
        highlightStars($('#rating').val());
    });

    $('.stars i').click(function () {
        var value = $(this).data('value');
        $('#rating').val(value);
    });

    function highlightStars(value) {
        $('.stars i').each(function () {
            var starValue = $(this).data('value');
            if (starValue <= value) {
                $(this).css('color', 'gold');
            } else {
                $(this).css('color', 'gray');
            }
        });
    }
});

// Configura el slider
$("#price-range").ionRangeSlider({
    type: "double",
    min: 0,
    max: 1000, // Cambia esto al valor máximo de tu rango de precios
    from: 100, // Valor inicial del rango
    to: 500,   // Valor inicial del rango
    prefix: "$",
    skin: "round", // Utiliza el skin "round" para cambiar el estilo
    onStart: function (data) {
        $("#price-range").val("$" + data.from + " - $" + data.to);
    },
    onChange: function (data) {
        $("#price-range").val("$" + data.from + " - $" + data.to);
    }
});

// Código JavaScript para abrir la ventana de filtros
document.getElementById('btnMostrarFiltros').addEventListener('click', function () {
    $('#filtroModal').modal('show');
});

// Código JavaScript para aplicar filtros y actualizar la lista de productos
document.getElementById('aplicarFiltros').addEventListener('click', function () {

    // Cierra la ventana de filtros
    $('#filtroModal').modal('hide');
});

window.addEventListener('scroll', function () {
    var navbar = document.querySelector('.navbar-con-fondo');
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-con-fondo-visible');
    } else {
        navbar.classList.remove('navbar-con-fondo-visible');
    }
});