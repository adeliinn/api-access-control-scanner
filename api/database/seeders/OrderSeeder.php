<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

class OrderSeeder extends Seeder
{
    public function run(): void
    {
        $alice = User::where('email', 'alice@example.test')->firstOrFail();
        $bob = User::where('email', 'bob@example.test')->firstOrFail();

        $orders = [
            [$alice, 'Laptop', 1200.00],
            [$alice, 'Keyboard', 80.00],
            [$bob, 'Smartphone', 1500.00],
        ];

        foreach ($orders as [$user, $description, $amount]) {
            $order = $user->orders()
                ->firstOrNew(['description' => $description]);

            $order->amount = $amount;
            $order->status = 'pending';
            $order->save();
        }
    }
}
