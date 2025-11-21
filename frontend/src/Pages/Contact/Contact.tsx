import { useState } from "react";
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
  Loader2,
} from "lucide-react";
import { toast } from "sonner";

interface FormData {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
}

const Contact = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    subject: "",
    message: "",
  });

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
      details: ["+1 (111) 111-11 11", "Call us anytime"],
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

const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const submitData = {
        ...formData,
        phone: formData.phone.trim() === "" ? null : formData.phone,
      };

      const res = await fetch(`${import.meta.env.VITE_API_URL}/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(submitData),
      });

      const json = await res.json();

      if (res.ok && json.status === "success") {
        toast.success("Message sent successfully!", {
          description: "We'll get back to you in 24 hours !",
        });
        
        setFormData({
          first_name: "",
          last_name: "",
          email: "",
          phone: "",
          subject: "",
          message: "",
        });
      } else {
        let errorMessage = "Please try again later !";
        
        if (json.detail) {
          if (Array.isArray(json.detail)) {
            errorMessage = json.detail.map((err: { msg: string }) => err.msg).join(", ");
          } else if (typeof json.detail === "string") {
            errorMessage = json.detail;
          }
        }
        
        toast.error("Failed to send message !", {
          description: errorMessage,
        });
      }
    } catch (error) {
      console.error("Contact form error : ", error);
      toast.error("Network error", {
        description: "Please check your connection and try again !",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">

      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 text-blue-400">
            Contact Us
          </h1>
          <p className="text-xl text-gray-300 leading-relaxed">
            Get in touch with Delicious Bites - We would love to hear from you!
          </p>
        </div>
      </section>

      {/* Contact Info */}
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

      {/* Contact Form and Map */}
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
                    <Label htmlFor="first_name" className="text-gray-300">
                      First Name *
                    </Label>
                    <Input
                      type="text"
                      id="first_name"
                      required
                      value={formData.first_name}
                      onChange={handleChange}
                      className="bg-gray-900 border-gray-700 text-white placeholder-gray-400 h-12"
                      placeholder="Your first name"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="last_name" className="text-gray-300">
                      Last Name *
                    </Label>
                    <Input
                      type="text"
                      id="last_name"
                      required
                      value={formData.last_name}
                      onChange={handleChange}
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
                    value={formData.email}
                    onChange={handleChange}
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
                    value={formData.phone}
                    onChange={handleChange}
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
                    value={formData.subject}
                    onChange={handleChange}
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
                    value={formData.message}
                    onChange={handleChange}
                    className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400 resize-vertical"
                    placeholder="Tell us how we can help you..."
                  />
                </div>

                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full cursor-pointer bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      Send Message
                    </>
                  )}
                </Button>
              </form>
            </div>

            {/* Map */}
            <div>
              <div className="flex items-center gap-3 mb-8">
                <Navigation className="w-8 h-8 text-blue-400" />
                <h2 className="text-3xl font-bold text-blue-400">Find Us</h2>
              </div>

              {/* Google Maps */}
              <div className="bg-gray-900 rounded-lg overflow-hidden mb-6">
                <iframe
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d50013.53788535637!2d27.12915445!3d38.42192095!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14bbd8e2fece48eb%3A0xafa58b890c33632a!2zS29uYWsvxLB6bWly!5e0!3m2!1str!2str!4v1763569596688!5m2!1str!2str"
                  width="100%"
                  height="400"
                  style={{ border: 0 }}
                  allowFullScreen
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  title="Delicious Bites Location"
                ></iframe>
              </div>

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