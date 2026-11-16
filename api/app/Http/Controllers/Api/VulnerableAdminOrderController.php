<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Order;
use Illuminate\Http\JsonResponse;

class VulnerableAdminOrderController extends Controller
{
    public function index(): JsonResponse
    {
        // Intentionally vulnerable: no admin role check.
        // For local security research only.
        return response()->json(Order::all());
    }
}
