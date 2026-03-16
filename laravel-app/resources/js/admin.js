import $ from 'jquery';
window.$ = window.jQuery = $;

import 'bootstrap';
import 'popper.js';
import 'admin-lte';
import OverlayScrollbars from 'overlayscrollbars';

document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.wrapper')) {
        OverlayScrollbars(document.querySelectorAll('.wrapper'), {});
    }
});

import '@fortawesome/fontawesome-free/js/all.min.js';