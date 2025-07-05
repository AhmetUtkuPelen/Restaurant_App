import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Define protected routes that require authentication
const protectedRoutes = ['/chat', '/users', '/profile', '/admin'];

// Define auth routes that should redirect to chat if already authenticated
const authRoutes = ['/login', '/register'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Get token from cookies, headers, or localStorage
  const cookieToken = request.cookies.get('token')?.value;
  const headerToken = request.headers.get('authorization')?.replace('Bearer ', '');
  
  // For client-side navigation, we need to check localStorage
  // This is a workaround since middleware runs on the server
  // In a real app, you might want to sync localStorage with cookies
  const localStorageToken = request.headers.get('x-auth-token');
  
  const token = cookieToken || headerToken || localStorageToken;

  // Check if the current path is a protected route
  const isProtectedRoute = protectedRoutes.some(route => 
    pathname.startsWith(route)
  );

  // Check if the current path is an auth route
  const isAuthRoute = authRoutes.some(route => 
    pathname.startsWith(route)
  );

  // If accessing a protected route without a token, redirect to login
  if (isProtectedRoute && !token) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // If accessing an auth route with a token, redirect to chat
  if (isAuthRoute && token) {
    return NextResponse.redirect(new URL('/chat', request.url));
  }

  // Admin route protection - this is a basic check, 
  // you might want to decode the JWT to check the role
  if (pathname.startsWith('/admin') && token) {
    // For now, we'll let the component handle admin role checking
    // In a production app, you'd want to decode the JWT here
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder files
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
