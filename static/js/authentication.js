$(document).ready(function () {
    // Ocultar inicialmente uno de los formularios en la ventana modal
    $("#formulario2").hide();

    // Función para mostrar el formulario 1 en la ventana modal y resaltar el botón
    $("#mostrarFormulario1").click(function () {
        if (!$("#formulario1").hasClass("formulario-activa")) {
            $("#formulario2").fadeOut(100, function () {
                $("#formulario1").fadeIn(100).addClass("formulario-activa");
                $("#formulario2").removeClass("formulario-activa");

                // Resaltar el botón del formulario 1 y desresaltar el del formulario 2
                $("#mostrarFormulario1").addClass("btn-primary");
                $("#mostrarFormulario2").removeClass("btn-primary");
            });
        }
    });

    function realizarSolicitudAjax() {
        // Realiza la solicitud AJAX para obtener el formulario
        $.ajax({
            type: "GET",
            url: createCustomerUrl,
            success: function (response) {
                $("#registration-form-container").html(response);
            }
        });
    }
    // Función para mostrar el formulario 2 en la ventana modal y resaltar el botón
    $("#mostrarFormulario2").click(function () {
        realizarSolicitudAjax();
        if (!$("#formulario2").hasClass("formulario-activa")) {
            $("#formulario1").fadeOut(100, function () {
                $("#formulario2").fadeIn(100).addClass("formulario-activa");
                $("#formulario1").removeClass("formulario-activa");

                // Resaltar el botón del formulario 2 y desresaltar el del formulario 1
                $("#mostrarFormulario2").addClass("btn-primary");
                $("#mostrarFormulario1").removeClass("btn-primary");
            });
        }
    });

    // Función para mostrar el formulario 2 cuando se hace clic en "Create new"
    $("#createNewBtn").click(function () {
        realizarSolicitudAjax();
        $("#formulario1").fadeOut(100, function () {
            $("#formulario2").fadeIn(100).addClass("formulario-activa");
            $("#formulario1").removeClass("formulario-activa");

            // Resaltar el botón del formulario 2 y desresaltar el del formulario 1
            $("#mostrarFormulario2").addClass("btn-primary");
            $("#mostrarFormulario1").removeClass("btn-primary");
        });
    });

    // Función para mostrar el formulario 1 cuando se hace clic en "Login here"
    // $("#loginHereBtn").click(function () {
    //     $("#formulario2").fadeOut(100, function () {
    //         $("#formulario1").fadeIn(100).addClass("formulario-activa");
    //         $("#formulario2").removeClass("formulario-activa");

    //         // Resaltar el botón del formulario 1 y desresaltar el del formulario 2
    //         $("#mostrarFormulario1").addClass("btn-primary");
    //         $("#mostrarFormulario2").removeClass("btn-primary");
    //     });
    // });

    // Mostrar inicialmente el formulario 1 y resaltarlo
    $("#formulario1").addClass("formulario-activa");
    $("#mostrarFormulario1").addClass("btn-primary");

});