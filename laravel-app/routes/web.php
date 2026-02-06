<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return 'Weather Platform - Bienvenido';
});

Route::get('/login', function () {
    return 'Página de Login (SP-001-F pendiente)';
})->name('login');

Route::get('/dashboard', function () {
    return 'Dashboard - Usuario autenticado';
})->middleware(['auth'])->name('dashboard');

Route::get('/admin/test', function () {
    return 'Panel Admin - Solo administradores';
})->middleware(['auth', 'is.admin'])->name('admin.test');