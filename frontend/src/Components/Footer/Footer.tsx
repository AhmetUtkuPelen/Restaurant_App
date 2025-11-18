
import { Link } from "react-router-dom";
import { 
  Facebook, 
  Instagram, 
  Twitter, 
  Youtube,
  MapPin,
  Phone,
  Mail,
  Clock
} from "lucide-react";
import Logo from "../../assets/logo.png"

const Footer = () => {

  const currentYear = new Date().getFullYear();

  const socialLinks = [
    { 
      name: "Facebook", 
      href: "https://github.com/AhmetUtkuPelen", 
      icon: <Facebook className="w-5 h-5" />,
      color: "hover:text-blue-500"
    },
    { 
      name: "Instagram", 
      href: "https://github.com/AhmetUtkuPelen", 
      icon: <Instagram className="w-5 h-5" />,
      color: "hover:text-pink-500"
    },
    { 
      name: "Twitter", 
      href: "https://github.com/AhmetUtkuPelen", 
      icon: <Twitter className="w-5 h-5" />,
      color: "hover:text-blue-400"
    },
    { 
      name: "YouTube", 
      href: "https://github.com/AhmetUtkuPelen", 
      icon: <Youtube className="w-5 h-5" />,
      color: "hover:text-red-500"
    },
  ];

  const quickLinks = [
    { name: "About Us", href: "/about" },
    { name: "Reservations", href: "/userReservations" },
    { name: "Contact", href: "/contact" },
    { name: "Terms of Service", href: "/terms" },
  ];

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main Footer Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Logo and Description */}
          <div className="text-center md:text-left">
            <Link to="/" className="flex items-center gap-3 mb-4 justify-center md:justify-start">
              <img 
                src={Logo} 
                alt="Delicious Bites Logo"
                className="w-12 h-12 rounded-lg"
              />
              <div>
                <h3 className="text-xl font-bold text-blue-400">Delicious Bites</h3>
              </div>
            </Link>
            <p className="text-gray-400 mb-4 leading-relaxed">
              Bringing authentic flavors to your table since 1995. 
              Experience the taste of tradition with every bite.
            </p>
            {/* Social Media Links */}
            <div className="flex gap-4 justify-center md:justify-start">
              {socialLinks.map((social) => (
                <a
                  key={social.name}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`text-gray-400 ${social.color} transition-colors p-2 bg-gray-800 rounded-lg hover:bg-gray-700`}
                  aria-label={social.name}
                >
                  {social.icon}
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div className="text-center md:text-left">
            <h4 className="text-lg font-semibold mb-4 text-blue-400">Quick Links</h4>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Information */}
          <div className="text-center md:text-left">
            <h4 className="text-lg font-semibold mb-4 text-blue-400">Contact Info</h4>
            <div className="space-y-3">
              <div className="flex items-start gap-3 justify-center md:justify-start">
                <MapPin className="w-5 h-5 text-blue-400 mt-0.5" />
                <div>
                  <p className="text-gray-400">123 Food Street</p>
                  <p className="text-gray-400">City Center, NY 10001</p>
                </div>
              </div>
              <div className="flex items-center gap-3 justify-center md:justify-start">
                <Phone className="w-5 h-5 text-blue-400" />
                <p className="text-gray-400">+1 (111) 111-11 11</p>
              </div>
              <div className="flex items-center gap-3 justify-center md:justify-start">
                <Mail className="w-5 h-5 text-blue-400" />
                <p className="text-gray-400">info@deliciousbites.com</p>
              </div>
              <div className="flex items-start gap-3 justify-center md:justify-start">
                <Clock className="w-5 h-5 text-blue-400 mt-0.5" />
                <div>
                  <p className="text-gray-400">Mon-Sun</p>
                  <p className="text-gray-400">11:00 AM - 10:00 PM</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Footer */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            {/* Copyright */}
            <div className="text-center md:text-left">
              <p className="text-gray-400">
                © {currentYear} Delicious Bites. All rights reserved.
              </p>
              <p className="text-sm text-gray-500">
                Made with ❤️ for food lovers everywhere
              </p>
            </div>

            {/* Additional Links */}
            <div className="flex gap-6 text-sm">
              <Link to="/terms" className="text-gray-400 hover:text-white transition-colors">
                Terms of Service
              </Link>
              <Link to="/about-dev" className="text-gray-400 hover:text-white transition-colors">
                About Developer
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
