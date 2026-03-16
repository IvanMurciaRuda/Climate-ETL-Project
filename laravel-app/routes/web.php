<?php

use App\Http\Controllers\Auth\LoginController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return 'Weather Platform - Bienvenido';
});

Route::get('/login', [LoginController::class,'showLoginForm'])->name('login');
Route::post('/login', [LoginController::class, 'login']);
Route::get('/logout', [LoginController::class ,'logout'])->name('logout');

Route::get('/dashboard', function () {
    return 'Dashboard - Usuario autenticado';
})->middleware(['auth'])->name('dashboard');

Route::get('/admin/test', function () {
    return 'Panel Admin - Solo administradores';
})->middleware(['auth', 'is.admin'])->name('admin.test');