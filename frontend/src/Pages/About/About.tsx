import { Card, CardContent } from "@/Components/ui/card";
import { MapPin, Clock, Phone, Mail, Users, Award, Heart } from "lucide-react";
import RestaurantImg from "../../assets/restaurant.png"

const About = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 text-blue-400">
            About Delicious Bites
          </h1>
          <p className="text-xl text-gray-300 leading-relaxed">
            Bringing authentic Mediterranean flavors to your table since 1995
          </p>
        </div>
      </section>

      {/* Restaurant Information */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-6 text-blue-400">Our Story</h2>
              <p className="text-gray-300 mb-6 leading-relaxed">
                Delicious Bites was founded in 1995 with a simple mission: to bring the authentic tastes 
                of the Mediterranean to our community. What started as a small family restaurant has grown 
                into a beloved dining destination, but we've never forgotten our roots.
              </p>
              <p className="text-gray-300 mb-6 leading-relaxed">
                Our recipes have been passed down through generations, combining traditional cooking methods 
                with the freshest local ingredients. Every dish tells a story of heritage, passion, and 
                dedication to culinary excellence.
              </p>
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center gap-2 text-blue-400">
                  <Users className="w-5 h-5" />
                  <span>Family Owned</span>
                </div>
                <div className="flex items-center gap-2 text-blue-400">
                  <Award className="w-5 h-5" />
                  <span>Award Winning</span>
                </div>
                <div className="flex items-center gap-2 text-blue-400">
                  <Heart className="w-5 h-5" />
                  <span>Made with Love</span>
                </div>
              </div>
            </div>
            <div className="relative">
              <img 
                src={RestaurantImg}
                alt="Restaurant Interior"
                className="rounded-lg shadow-2xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* What We Do */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">What We Do</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center bg-gray-900 border-gray-700">
              <CardContent className="pt-6">
                <div className="text-blue-400 mb-4 flex justify-center">
                  <Users className="w-12 h-12" />
                </div>
                <h3 className="text-xl font-semibold mb-4 text-white">Dine-In Experience</h3>
                <p className="text-gray-400">
                  Enjoy our warm, welcoming atmosphere with exceptional service and authentic Mediterranean ambiance.
                </p>
              </CardContent>
            </Card>
            <Card className="text-center bg-gray-900 border-gray-700">
              <CardContent className="pt-6">
                <div className="text-blue-400 mb-4 flex justify-center">
                  <Clock className="w-12 h-12" />
                </div>
                <h3 className="text-xl font-semibold mb-4 text-white">Online Ordering</h3>
                <p className="text-gray-400">
                  Order your favorite dishes online for quick pickup or convenient delivery to your doorstep.
                </p>
              </CardContent>
            </Card>
            <Card className="text-center bg-gray-900 border-gray-700">
              <CardContent className="pt-6">
                <div className="text-blue-400 mb-4 flex justify-center">
                  <Heart className="w-12 h-12" />
                </div>
                <h3 className="text-xl font-semibold mb-4 text-white">Catering Services</h3>
                <p className="text-gray-400">
                  Let us cater your special events with our delicious Mediterranean cuisine and professional service.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Contact Info */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">Visit Us</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-semibold mb-6">Contact Information</h3>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <MapPin className="w-6 h-6 text-blue-400" />
                  <div>
                    <p className="font-semibold">Address</p>
                    <p className="text-gray-400">123 Food Street, City Center, NY 10001</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Phone className="w-6 h-6 text-blue-400" />
                  <div>
                    <p className="font-semibold">Phone</p>
                    <p className="text-gray-400">+1 (111) 111-11 11</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Mail className="w-6 h-6 text-blue-400" />
                  <div>
                    <p className="font-semibold">Email</p>
                    <p className="text-gray-400">info@deliciousbites.com</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Clock className="w-6 h-6 text-blue-400" />
                  <div>
                    <p className="font-semibold">Hours</p>
                    <p className="text-gray-400">Mon-Sun: 11:00 AM - 10:00 PM</p>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <h3 className="text-2xl font-semibold mb-6">Location</h3>
              <div className="bg-gray-800 rounded-lg overflow-hidden">
                <iframe
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d50013.53788535637!2d27.12915445!3d38.42192095!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14bbd8e2fece48eb%3A0xafa58b890c33632a!2zS29uYWsvxLB6bWly!5e0!3m2!1str!2str!4v1763569596688!5m2!1str!2str"
                  width="100%"
                  height="300"
                  style={{ border: 0 }}
                  allowFullScreen
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  title="Restaurant Location"
                ></iframe>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;