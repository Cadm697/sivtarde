var eliminando;
var bandera = 1;
function cambiaRuta(ruta) {
    if(bandera == 1){
        let frm = document.getElementById("formulario");
        frm.action = ruta;
        eliminando = false;
        bandera = 20;
    } else {
        if(ruta == "/productos/save"){
            ruta = "/save" 
            let frm = document.getElementById("formulario");
            frm.action = ruta;
            eliminando = false;
            bandera = 20;
        } else if (ruta == "/productos/get"){
            ruta = "/get" 
            let frm = document.getElementById("formulario");
            frm.action = ruta;
            eliminando = false;
            bandera = 20;
        } else if (ruta == "/productos/update"){
            ruta = "/update" 
            let frm = document.getElementById("formulario");
            frm.action = ruta;
            eliminando = false;
            bandera = 20;
        } else {
            ruta = "/delete" 
            let frm = document.getElementById("formulario");
            frm.action = ruta;
            eliminando = false;
            bandera = 20;
        }
    }
    if(ruta == "/productos/delete") {
        eliminando = true;
    }
}

function confirmarBorrado(){
    if(eliminando){
        let resp = confirm("¿Desea realmente borrar el registro?");
        return resp;
    }
    return true;
}