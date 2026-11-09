<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Order;
use Illuminate\Http\JsonResponse;

class VulnerableOrderController extends Controller
{
    public function show(int $id): JsonResponse
    {
        abort_unless(app()->environment('local'), 404);

        $order = Order::findOrFail($id);

        return response()->json($order);
    }
}
