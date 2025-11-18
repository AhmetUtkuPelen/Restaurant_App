import { useState } from "react";
import { Button } from "@/Components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/Components/ui/dropdown-menu";
import {
  Menu,
  X,
  ShoppingCart,
  User,
  Heart,
  Settings,
  LogOut,
  ChevronDown,
  LogIn,
  UserPlus,
  UtensilsCrossed,
} from "lucide-react";
import { Link } from "react-router-dom";
import { useCartStore } from "@/Zustand/Cart/CartState";
import { useAuthStore } from "@/Zustand/Auth/AuthState";
import Logo from "../../assets/logo.png"

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [isMenuDropdownOpen, setIsMenuDropdownOpen] = useState(false);

  // Cart total items
  const totalItems = useCartStore((state) => state.getTotalItems());

  // Authentication state
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  const navigationLinks = [
    { name: "HOME", href: "/" },
    { name: "ABOUT", href: "/about" },
    { name: "CONTACT", href: "/contact" },
  ];

  const menuCategories = [
    { name: "DESSERTS", href: "/desserts" },
    { name: "DRINKS", href: "/drinks" },
    { name: "SALADS", href: "/salads" },
    { name: "DONERS", href: "/doners" },
    { name: "KEBABS", href: "/kebabs" },
  ];

  const userMenuItems = [
    { name: "Profile", href: "/profile", icon: <User className="w-4 h-4" /> },
    {
      name: "Orders",
      href: "/userOrders",
      icon: <ShoppingCart className="w-4 h-4" />,
    },
    {
      name: "Favorites",
      href: "/favouriteProducts",
      icon: <Heart className="w-4 h-4" />,
    },
    {
      name: "Reservations",
      href: "/userReservations",
      icon: <UtensilsCrossed className="w-4 h-4" />,
    },
    {
      name: "Settings",
      href: "/settings",
      icon: <Settings className="w-4 h-4" />,
    },
  ];

  return (
    <header className="bg-gray-900 text-white shadow-lg sticky top-0 z-50">

      {/* Main Header */}
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <img
              src={Logo}
              alt="Delicious Bites Restaurant Logo"
              className="w-24 h-12 rounded-lg"
            />
            <span className="text-lg font-bold text-blue-400">Delicious Bites</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center text-center space-x-8">
            {navigationLinks.map((link) => (
              <Link
                key={link.name}
                to={link.href}
                className="text-gray-300 hover:text-blue-400 transition-colors font-medium items-center"
              >
                {link.name}
              </Link>
            ))}

            {/* Menu Dropdown */}
            <DropdownMenu
              open={isMenuDropdownOpen}
              onOpenChange={setIsMenuDropdownOpen}
            >
              <div
                onMouseEnter={() => setIsMenuDropdownOpen(true)}
                onMouseLeave={() => setIsMenuDropdownOpen(false)}
              >
                <DropdownMenuTrigger asChild>
                  <Link
                    to="/"
                    className="text-gray-300 hover:text-blue-400 transition-colors font-medium flex items-center gap-1 outline-none"
                    onClick={(e) => {
                      if (!isMenuDropdownOpen) {
                        return;
                      }
                      e.preventDefault();
                    }}
                  >
                    MENU
                    <ChevronDown
                      className={`w-4 h-4 transition-transform ${
                        isMenuDropdownOpen ? "rotate-180" : ""
                      }`}
                    />
                  </Link>
                </DropdownMenuTrigger>

                <DropdownMenuContent
                  className="w-48 bg-gray-800 border-gray-700 text-gray-300"
                  align="start"
                  onMouseEnter={() => setIsMenuDropdownOpen(true)}
                  onMouseLeave={() => setIsMenuDropdownOpen(false)}
                >
                  {menuCategories.map((category) => (
                    <DropdownMenuItem key={category.name} asChild>
                      <Link
                        to={category.href}
                        className="text-gray-300 hover:text-blue-400 hover:bg-gray-700 focus:text-blue-400 focus:bg-gray-700 cursor-pointer"
                        onClick={() => setIsMenuDropdownOpen(false)}
                      >
                        {category.name}
                      </Link>
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </div>
            </DropdownMenu>
          </nav>

          {/* Right Side */}
          <div className="flex items-center gap-4">
            {/* Show Cart and User Menu if authenticated */}
            {isAuthenticated ? (
              <>
                {/* Cart */}
                <Link to="/cart">
                  <Button
                    variant="ghost"
                    className="relative hover:bg-blue-400 cursor-pointer"
                  >
                    <ShoppingCart className="w-6 h-6" />
                    {totalItems > 0 && (
                      <span className="absolute -top-2 -right-2 bg-blue-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {totalItems}
                      </span>
                    )}
                  </Button>
                </Link>

                {/* User Dropdown */}
                <div className="relative">
                  <Button
                    variant="ghost"
                    onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                    className="hover:bg-blue-400 flex items-center gap-2 cursor-pointer"
                  >
                    <User className="w-5 h-5" />
                    {user && (
                      <span className="hidden md:inline text-sm">
                        {user.username}
                      </span>
                    )}
                  </Button>

                  {/* User Dropdown Menu */}
                  {isUserMenuOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-lg py-2 z-50">
                      {/* User Info */}
                      {user && (
                        <>
                          <div className="px-4 py-2 border-b border-gray-700">
                            <p className="text-md font-medium text-white">
                              {user.username}
                            </p>
                            <p className="text-md text-gray-400">
                              {user.email}
                            </p>
                          </div>
                        </>
                      )}

                      {userMenuItems.map((item) => (
                        <Link
                          key={item.name}
                          to={item.href}
                          className="flex items-center gap-3 px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
                          onClick={() => setIsUserMenuOpen(false)}
                        >
                          {item.icon}
                          {item.name}
                        </Link>
                      ))}
                      <hr className="my-2 border-gray-700" />
                      <Button
                        onClick={() => {
                          logout();
                          setIsUserMenuOpen(false);
                        }}
                        className="flex cursor-pointer items-center gap-3 px-4 py-2 text-red-500 hover:bg-gray-700 hover:text-white transition-colors w-full text-left"
                      >
                        <LogOut className="w-4 h-4 text-red-500" />
                        Log Out
                      </Button>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <>
                {/* Login and Register buttons for non-authenticated users */}
                <Link to="/login">
                  <Button
                    variant="ghost"
                    className="hover:bg-blue-400 flex items-center gap-2 cursor-pointer"
                  >
                    <LogIn className="w-4 h-4" />
                    <span className="hidden md:inline">LOGIN</span>
                  </Button>
                </Link>
                <Link to="/register">
                  <Button className="hover:bg-blue-400 cursor-pointer flex items-center gap-2">
                    <UserPlus className="w-4 h-4" />
                    <span className="hidden md:inline">REGISTER</span>
                  </Button>
                </Link>
              </>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              className="lg:hidden hover:bg-gray-800"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <nav className="lg:hidden mt-4 pb-4 border-t border-gray-700 pt-4">
            <div className="flex flex-col space-y-3">
              {navigationLinks.map((link) => (
                <Link
                  key={link.name}
                  to={link.href}
                  className="text-gray-300 hover:text-blue-400 transition-colors font-medium py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {link.name}
                </Link>
              ))}

              {/* Mobile Menu Categories */}
              <div className="pt-2 border-t border-gray-700">
                {menuCategories.map((category) => (
                  <Link
                    key={category.name}
                    to={category.href}
                    className="block text-gray-300 hover:text-blue-400 transition-colors py-2 pl-4"
                    onClick={() => setIsMenuOpen(false)}
                  >
                      {category.name}
                  </Link>
                ))}
              </div>

              {/* Mobile Auth Section */}
              <div className="pt-2 border-t border-gray-700">
                {isAuthenticated ? (
                  <>
                    {/* User Info */}
                    {user && (
                      <div className="px-2 py-2 mb-2">
                        <p className="text-sm font-medium text-white">
                          {user.username}
                        </p>
                        <p className="text-xs text-gray-400">{user.email}</p>
                      </div>
                    )}

                    {/* Cart Link */}
                    <Link
                      to="/cart"
                      className="flex items-center gap-3 text-gray-300 hover:text-blue-400 transition-colors py-2"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <ShoppingCart className="w-4 h-4" />
                      Cart
                      {totalItems > 0 && (
                        <span className="bg-blue-500 text-white text-xs rounded-full px-2 py-0.5">
                          {totalItems}
                        </span>
                      )}
                    </Link>

                    {/* User Menu Items */}
                    {userMenuItems.map((item) => (
                      <Link
                        key={item.name}
                        to={item.href}
                        className="flex items-center gap-3 text-gray-300 hover:text-blue-400 transition-colors py-2"
                        onClick={() => setIsMenuOpen(false)}
                      >
                        {item.icon}
                        {item.name}
                      </Link>
                    ))}

                    {/* Logout */}
                    <Button
                      onClick={() => {
                        logout();
                        setIsMenuOpen(false);
                      }}
                      className="flex items-center gap-3 text-gray-300 hover:text-red-400 transition-colors py-2 w-full text-left mt-2"
                    >
                      <LogOut className="w-4 h-4" />
                      Log Out
                    </Button>
                  </>
                ) : (
                  <>
                    {/* Login and Register for non-authenticated users */}
                <Link to="/login">
                  <Button
                    variant="ghost"
                    className="hover:bg-blue-400 flex items-center gap-2 cursor-pointer"
                  >
                    <LogIn className="w-4 h-4" />
                    <span className="hidden md:inline">LOGIN</span>
                  </Button>
                </Link>
                <Link to="/register">
                  <Button className="hover:bg-blue-400 cursor-pointer flex items-center gap-2">
                    <UserPlus className="w-4 h-4" />
                    <span className="hidden md:inline">REGISTER</span>
                  </Button>
                </Link>
                  </>
                )}
              </div>
            </div>
          </nav>
        )}
      </div>

      {/* Click outside to close dropdowns */}
      {(isUserMenuOpen || isMenuOpen) && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => {
            setIsUserMenuOpen(false);
            setIsMenuOpen(false);
            setIsMenuDropdownOpen(false);
          }}
        />
      )}
    </header>
  );
};

export default Header;
