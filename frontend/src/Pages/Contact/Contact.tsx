import { Button } from "@/Components/ui/button";
import { Input } from "@/Components/ui/input";
import { Label } from "@/Components/ui/label";
import { Card, CardContent } from "@/Components/ui/card";
import {
  MapPin,
  Phone,
  Mail,
  Clock,
  Send,
  MessageSquare,
  Navigation,
  Calendar,
} from "lucide-react";

const Contact = () => {
  const contactInfo = [
    {
      icon: <MapPin className="w-6 h-6" />,
      title: "Address",
      details: ["123 Food Street", "City Center, NY 10001"],
      color: "text-blue-400",
    },
    {
      icon: <Phone className="w-6 h-6" />,
      title: "Phone",
      details: ["+1 (555) 123-4567", "Call us anytime"],
      color: "text-green-400",
    },
    {
      icon: <Mail className="w-6 h-6" />,
      title: "Email",
      details: ["info@deliciousbites.com", "We'll respond within 24 hours"],
      color: "text-purple-400",
    },
    {
      icon: <Clock className="w-6 h-6" />,
      title: "Hours",
      details: ["Mon-Sun: 11:00 AM - 10:00 PM", "Kitchen closes at 9:30 PM"],
      color: "text-orange-400",
    },
  ];

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  const formData = {
    first_name: (document.getElementById("firstName") as HTMLInputElement).value,
    last_name: (document.getElementById("lastName") as HTMLInputElement).value,
    email: (document.getElementById("email") as HTMLInputElement).value,
    phone: (document.getElementById("phone") as HTMLInputElement).value,
    subject: (document.getElementById("subject") as HTMLSelectElement).value,
    message: (document.getElementById("message") as HTMLTextAreaElement).value,
  };

  const res = await fetch("http://localhost:8000/contact", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  const json = await res.json();

  if (json.status === "ok") {
    alert("Message sent successfully!");
  } else {
    alert("Error sending message.");
  }
};

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 text-blue-400">
            Contact Us
          </h1>
          <p className="text-xl text-gray-300 leading-relaxed">
            Get in touch with Delicious Bites - We'd love to hear from you!
          </p>
        </div>
      </section>

      {/* Contact Information Cards */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {contactInfo.map((info, index) => (
              <Card
                key={index}
                className="bg-gray-800 border-gray-700 text-center hover:bg-gray-700 transition-colors"
              >
                <CardContent className="pt-6">
                  <div className={`${info.color} mb-4 flex justify-center`}>
                    {info.icon}
                  </div>
                  <h3 className="text-lg font-semibold mb-3 text-white">
                    {info.title}
                  </h3>
                  {info.details.map((detail, idx) => (
                    <p
                      key={idx}
                      className={
                        idx === 0
                          ? "text-gray-300 font-medium"
                          : "text-gray-400 text-sm"
                      }
                    >
                      {detail}
                    </p>
                  ))}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form and Map Section */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div>
              <div className="flex items-center gap-3 mb-8">
                <MessageSquare className="w-8 h-8 text-blue-400" />
                <h2 className="text-3xl font-bold text-blue-400">
                  Send us a Message
                </h2>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="firstName" className="text-gray-300">
                      First Name *
                    </Label>
                    <Input
                      type="text"
                      id="firstName"
                      required
                      className="bg-gray-900 border-gray-700 text-white placeholder-gray-400 h-12"
                      placeholder="Your first name"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="lastName" className="text-gray-300">
                      Last Name *
                    </Label>
                    <Input
                      type="text"
                      id="lastName"
                      required
                      className="bg-gray-900 border-gray-700 text-white placeholder-gray-400 h-12"
                      placeholder="Your last name"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email" className="text-gray-300">
                    Email Address *
                  </Label>
                  <Input
                    type="email"
                    id="email"
                    required
                    className="bg-gray-900 border-gray-700 text-white placeholder-gray-400 h-12"
                    placeholder="your.email@example.com"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="phone" className="text-gray-300">
                    Phone Number
                  </Label>
                  <Input
                    type="tel"
                    id="phone"
                    className="bg-gray-900 border-gray-700 text-white placeholder-gray-400 h-12"
                    placeholder="+1 (555) 123-4567"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="subject" className="text-gray-300">
                    Subject *
                  </Label>
                  <select
                    id="subject"
                    required
                    className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400 h-12"
                  >
                    <option value="">Select a subject</option>
                    <option value="reservation">Table Reservation</option>
                    <option value="catering">Catering Inquiry</option>
                    <option value="feedback">Feedback</option>
                    <option value="complaint">Complaint</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="message" className="text-gray-300">
                    Message *
                  </Label>
                  <textarea
                    id="message"
                    required
                    rows={5}
                    className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400 resize-vertical"
                    placeholder="Tell us how we can help you..."
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg flex items-center justify-center gap-2"
                >
                  <Send className="w-5 h-5" />
                  Send Message
                </Button>
              </form>
            </div>

            {/* Map and Location Info */}
            <div>
              <div className="flex items-center gap-3 mb-8">
                <Navigation className="w-8 h-8 text-blue-400" />
                <h2 className="text-3xl font-bold text-blue-400">Find Us</h2>
              </div>

              {/* Google Map */}
              <div className="bg-gray-900 rounded-lg overflow-hidden mb-6">
                <iframe
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.9663095343008!2d-74.00425878459418!3d40.74844097932681!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259a9b3117469%3A0xd134e199a405a163!2sEmpire%20State%20Building!5e0!3m2!1sen!2sus!4v1635959542165!5m2!1sen!2sus"
                  width="100%"
                  height="400"
                  style={{ border: 0 }}
                  allowFullScreen
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  title="Delicious Bites Location"
                ></iframe>
              </div>

              {/* Location Details */}
              <Card className="bg-gray-900 border-gray-700">
                <CardContent className="p-6">
                  <h3 className="text-xl font-semibold mb-4 text-blue-400">
                    Location Details
                  </h3>
                  <div className="space-y-4">
                    <div className="flex items-start gap-3">
                      <MapPin className="w-5 h-5 text-blue-400 mt-1" />
                      <div>
                        <p className="font-medium text-white">
                          Delicious Bites Restaurant
                        </p>
                        <p className="text-gray-400">123 Food Street</p>
                        <p className="text-gray-400">City Center, NY 10001</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <Calendar className="w-5 h-5 text-blue-400" />
                      <div>
                        <p className="font-medium text-white">
                          Parking Available
                        </p>
                        <p className="text-gray-400">
                          Free parking for customers
                        </p>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-gray-700">
                      <p className="text-gray-400 text-sm">
                        Located in the heart of the city, easily accessible by
                        public transport. We're just a 5-minute walk from the
                        subway station.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact;
