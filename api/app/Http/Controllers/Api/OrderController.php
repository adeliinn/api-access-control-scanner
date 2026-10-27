<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Order;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class OrderController extends Controller
{
    public function index(Request $request)
    {
        $user = $request->user();

        $orders = $user->role === 'admin'
            ? Order::all()
            : $user->orders()->get();

        return response()->json($orders);
    }

    public function show(Request $request, int $id): JsonResponse
    {
        $order = Order::findOrFail($id);

        Gate::authorize('view', $order);

        return response()->json($order);
    }

    public function store(Request $request): JsonResponse
    {
        Gate::authorize('create', Order::class);

        $validated = $request->validate([
            'description' => ['required', 'string', 'max:255'],
            'amount' => ['required', 'numeric', 'gt:0'],
        ]);

        $order = $request->user()->orders()->create([
            'description' => $validated['description'],
            'amount' => $validated['amount'],
            'status' => 'pending',
        ]);

        return response()->json($order, 201);
    }

    public function update(Request $request, int $id): JsonResponse
    {
        $order = Order::findOrFail($id);

        Gate::authorize('update', $order);

        $validated = $request->validate([
            'description' => ['required', 'string', 'max:255'],
            'amount' => ['required', 'numeric', 'gt:0'],
        ]);

        $order->update($validated);

        return response()->json($order);
    }

    public function destroy(Request $request, int $id): JsonResponse
    {
        $order = Order::findOrFail($id);

        Gate::authorize('delete', $order);

        $order->delete();

        return response()->json(null, 204);
    }
}
