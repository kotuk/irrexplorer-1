import React from 'react';
import ReactDOM from 'react-dom';

import App from './App';

import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import '@popperjs/core/dist/esm/popper'
import Footer from "./components/footer";
window.bootstrap = require('bootstrap/dist/js/bootstrap.bundle.js');

ReactDOM.render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>,
    document.getElementById('root')
);


ReactDOM.render(
    <React.StrictMode>
        <Footer/>
    </React.StrictMode>,
    document.getElementById('footer')
);

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new window.bootstrap.Popover(popoverTriggerEl)
})
