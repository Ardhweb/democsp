// import Swal from 'sweetalert2'

// // or via CommonJS
// const Swal = require('sweetalert2')
// import Swal from 'sweetalert2/dist/sweetalert2.js'
// import 'sweetalert2/src/sweetalert2.scss'
// import 'sweetalert2/themes/bootstrap-5.css'

// Swal.fire({
//   title: 'Bootstrap 5 theme',
//   theme: 'bootstrap-5'
//   // theme: 'bootstrap-5-light' // light theme only
//   // theme: 'bootstrap-5-dark' // dark theme only
// })
function testAlert() {
    Swal.fire({
        title: 'Bootstrap 5 theme',
        text: 'SweetAlert2 is working!',
        icon: 'success',
        confirmButtonText: 'OK'
    })
}