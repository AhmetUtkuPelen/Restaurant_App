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
  Phone,
  Clock,
  ChevronDown
} from "lucide-react";
import { Link } from "react-router-dom";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [isMenuDropdownOpen, setIsMenuDropdownOpen] = useState(false);

  const navigationLinks = [
    { name: "Home", href: "/" },
    { name: "About", href: "/about" },
    { name: "Reservations", href: "/reservations" },
    { name: "Contact", href: "/contact" },
  ];

  const menuCategories = [
    { name: "All Menu", href: "/menu" },
    { name: "Desserts", href: "/desserts" },
    { name: "Drinks", href: "/drinks" },
    { name: "Salads", href: "/salads" },
    { name: "Doners", href: "/doners" },
    { name: "Kebabs", href: "/kebabs" },
    { name: "Special Offers", href: "/specials" },
  ];

  const userMenuItems = [
    { name: "Profile", href: "/profile", icon: <User className="w-4 h-4" /> },
    { name: "Orders", href: "/orders", icon: <ShoppingCart className="w-4 h-4" /> },
    { name: "Favorites", href: "/favorites", icon: <Heart className="w-4 h-4" /> },
    { name: "Settings", href: "/settings", icon: <Settings className="w-4 h-4" /> },
  ];

  return (
    <header className="bg-gray-900 text-white shadow-lg sticky top-0 z-50">
      {/* Top Bar */}
      <div className="bg-gray-800 py-2 px-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center text-sm">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Phone className="w-4 h-4 text-blue-400" />
              <span>+1 (555) 123-4567</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-blue-400" />
              <span>Mon-Sun: 11:00 AM - 10:00 PM</span>
            </div>
          </div>
          <div className="hidden md:block">
            <span className="text-blue-400">Free delivery on orders over $30!</span>
          </div>
        </div>
      </div>

      {/* Main Header */}
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <img 
              src="https://via.placeholder.com/50x50/3b82f6/ffffff?text=DB" 
              alt="Delicious Bites Logo"
              className="w-12 h-12 rounded-lg"
            />
            <div>
              <h1 className="text-xl font-bold text-blue-400">Delicious Bites</h1>
              <p className="text-xs text-gray-400">Mediterranean Cuisine</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            {navigationLinks.map((link) => (
              <Link
                key={link.name}
                to={link.href}
                className="text-gray-300 hover:text-blue-400 transition-colors font-medium"
              >
                {link.name}
              </Link>
            ))}
            
            {/* Menu Dropdown using ShadCN */}
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
                    to="/menu"
                    className="text-gray-300 hover:text-blue-400 transition-colors font-medium flex items-center gap-1 outline-none"
                    onClick={(e) => {
                      // Allow navigation to /menu when clicking directly on the link
                      if (!isMenuDropdownOpen) {
                        return;
                      }
                      e.preventDefault();
                    }}
                  >
                    Menu
                    <ChevronDown 
                      className={`w-4 h-4 transition-transform ${isMenuDropdownOpen ? 'rotate-180' : ''}`}
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

          {/* Right Side Actions */}
          <div className="flex items-center gap-4">
            {/* Cart Button */}
            <Button 
              variant="ghost" 
              className="relative hover:bg-gray-800"
            >
              <ShoppingCart className="w-5 h-5" />
              <span className="absolute -top-2 -right-2 bg-blue-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                3
              </span>
            </Button>

            {/* User Dropdown */}
            <div className="relative">
              <Button
                variant="ghost"
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="hover:bg-gray-800"
              >
                <User className="w-5 h-5" />
              </Button>

              {/* User Dropdown Menu */}
              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-lg py-2 z-50">
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
                  <button className="flex items-center gap-3 px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors w-full text-left">
                    <LogOut className="w-4 h-4" />
                    Sign Out
                  </button>
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              className="lg:hidden hover:bg-gray-800"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
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
                <p className="text-blue-400 font-medium mb-2">Menu Categories</p>
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