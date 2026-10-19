<?php

use App\Http\Controllers\Api\AuthController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::post('/login', [AuthController::class, 'login'])
    ->middleware('throttle:5,1');
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
