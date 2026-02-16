<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Role;

class InitialUsersSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $users = [
            [
                "name" => "admin",
                "email" => "admin@email.com",
                "password"=> bcrypt("admin"),
                "role_id" => Role::ADMIN,
                "is_active"=> true,
            ],
            [
                "name" => "user",
                "email" => "user@email.com",
                "password"=> bcrypt("user"),
                "role_id" => Role::USER,
                "is_active"=> true,
            ],
        ];

        foreach ($users as $user) {
            User::firstOrCreate($user);
        }

        return;
    }
}
