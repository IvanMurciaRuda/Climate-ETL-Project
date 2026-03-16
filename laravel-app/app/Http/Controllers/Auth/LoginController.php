<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    public function showLoginForm(){
        return view('auth/login');
    }

    public function login(Request $request){
        $credentials = $request->validate([
            'email'=> 'required|email',
            'password'=> 'required'
        ]);

         if(Auth::attempt($credentials, $request->remember)){
            $request->session()->regenerate();

            if(auth()->user()->isAdmin()){
                return redirect()->intended('admin/dashboard');
            }

            return redirect()->intended('/dashboard');

        }

        return back()->withErrors([
            'email'=> 'incorrect credentials'
        ]);
    }

    public function logout(Request $request){
        auth()->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        
        return redirect('/');
    }
}
