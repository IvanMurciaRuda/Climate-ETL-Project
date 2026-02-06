<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use Auth;

class IsAdmin
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {

        if(!Auth::check()){
            return redirect()->route('login')->withErrors([
                'message' => 'Please, log in to access this page'
            ]);
        }

        $user = Auth::user();

        if(!$user->isActive()){
            Auth::logout();
            return redirect()->route('login')->withErrors([
                'message' => 'This account is deactivated, please contact the administrator'
            ]);
        }

        if(!$user->isAdmin()){
            return redirect()->route('dashboard')->withErrors([
                'message'=> "You don't have permission to access this content"
            ]);
        }
    
        return $next($request);
    }
}
