<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\OrderController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::post('/login', [AuthController::class, 'login'])
    ->middleware('throttle:5,1');
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
Route::get('/orders', [OrderController::class, 'index'])
    ->middleware('auth:sanctum');
Route::get('/orders/{id}', [OrderController::class, 'show'])
    ->whereNumber('id')
    ->middleware('auth:sanctum');
Route::post('/orders', [OrderController::class, 'store'])
    ->middleware('auth:sanctum');
Route::put('/orders/{id}', [OrderController::class, 'update'])
    ->whereNumber('id')
    ->middleware('auth:sanctum');
Route::delete('/orders/{id}', [OrderController::class, 'destroy'])
    ->whereNumber('id')
    ->middleware('auth:sanctum');
