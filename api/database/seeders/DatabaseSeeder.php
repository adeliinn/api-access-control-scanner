<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $users = [
            ['name' => 'Alice', 'email' => 'alice@example.test', 'role' => 'user'],
            ['name' => 'Bob', 'email' => 'bob@example.test', 'role' => 'user'],
            ['name' => 'Admin', 'email' => 'admin@example.test', 'role' => 'admin'],
        ];

        foreach ($users as $data) {
            $user = User::firstOrNew(['email' => $data['email']]);

            $user->name = $data['name'];
            $user->password = 'TestPassword123!';
            $user->role = $data['role'];

            $user->save();
        }
    }
}
