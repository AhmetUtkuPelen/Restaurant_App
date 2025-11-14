import { Card, CardContent } from "@/Components/ui/card";
import {
  Code,
  Database,
  Globe,
  Layers,
  Server,
  Smartphone,
} from "lucide-react";

const AboutDev = () => {
  const frontendTech = [
    {
      name: "React",
      description: "A JavaScript library for building user interfaces",
      icon: <Globe className="w-8 h-8" />,
      color: "text-blue-400",
    },
    {
      name: "TypeScript",
      description:
        "Typed superset of JavaScript that compiles to plain JavaScript",
      icon: <Code className="w-8 h-8" />,
      color: "text-blue-500",
    },
    {
      name: "TailwindCSS",
      description: "A utility-first CSS framework for rapid UI development",
      icon: <Layers className="w-8 h-8" />,
      color: "text-cyan-400",
    },
    {
      name: "ShadCN",
      description:
        "Beautifully designed components built with Radix UI and Tailwind CSS",
      icon: <Smartphone className="w-8 h-8" />,
      color: "text-gray-400",
    },
  ];

  const backendTech = [
    {
      name: "Python",
      description: "High-level programming language for backend development",
      icon: <Server className="w-8 h-8" />,
      color: "text-yellow-400",
    },
    {
      name: "FastAPI",
      description: "Modern, fast web framework for building APIs with Python",
      icon: <Globe className="w-8 h-8" />,
      color: "text-green-400",
    },
    {
      name: "SQLAlchemy",
      description: "Python SQL toolkit and Object-Relational Mapping library",
      icon: <Database className="w-8 h-8" />,
      color: "text-red-400",
    },
    {
      name: "Pydantic",
      description:
        "Data validation and settings management using Python type annotations",
      icon: <Code className="w-8 h-8" />,
      color: "text-purple-400",
    },
    {
      name: "PostgreSQL",
      description: "Advanced open source relational database",
      icon: <Database className="w-8 h-8" />,
      color: "text-blue-600",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 text-blue-400">
            About the Developer
          </h1>
          <p className="text-xl text-gray-300 leading-relaxed">
            Built with modern technologies for optimal performance and user
            experience
          </p>
        </div>
      </section>

      {/* Tech Stack Overview */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-6 text-blue-400">
              Technology Stack
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              This restaurant application is built using cutting-edge
              technologies to ensure scalability, performance, and
              maintainability.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Frontend Technologies */}
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-8">
                <div className="flex items-center gap-3 mb-8">
                  <Globe className="w-8 h-8 text-blue-400" />
                  <h3 className="text-3xl font-bold text-blue-400">Frontend</h3>
                </div>
                <div className="space-y-6">
                  {frontendTech.map((tech, index) => (
                    <Card
                      key={index}
                      className="bg-gray-900 border-gray-600 hover:bg-gray-700 transition-colors"
                    >
                      <CardContent className="flex items-start gap-4 p-4">
                        <div className={tech.color}>{tech.icon}</div>
                        <div>
                          <h4 className="text-xl font-semibold mb-2 text-white">
                            {tech.name}
                          </h4>
                          <p className="text-gray-400">{tech.description}</p>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Backend Technologies */}
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-8">
                <div className="flex items-center gap-3 mb-8">
                  <Server className="w-8 h-8 text-green-400" />
                  <h3 className="text-3xl font-bold text-green-400">Backend</h3>
                </div>
                <div className="space-y-6">
                  {backendTech.map((tech, index) => (
                    <Card
                      key={index}
                      className="bg-gray-900 border-gray-600 hover:bg-gray-700 transition-colors"
                    >
                      <CardContent className="flex items-start gap-4 p-4">
                        <div className={tech.color}>{tech.icon}</div>
                        <div>
                          <h4 className="text-xl font-semibold mb-2 text-white">
                            {tech.name}
                          </h4>
                          <p className="text-gray-400">{tech.description}</p>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Architecture Overview */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">
            Application Architecture
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center bg-gray-900 border-gray-700">
              <CardContent className="pt-6">
                <div className="text-blue-400 mb-4 flex justify-center">
                  <Smartphone className="w-12 h-12" />
                </div>
                <h3 className="text-xl font-semibold mb-4 text-white">
                  Responsive Design
                </h3>
                <p className="text-gray-400">
                  Mobile-first approach ensuring optimal experience across all
                  devices and screen sizes.
                </p>
              </CardContent>
            </Card>
            <Card className="text-center bg-gray-900 border-gray-700">
              <CardContent className="pt-6">
                <div className="text-green-400 mb-4 flex justify-center">
                  <Server className="w-12 h-12" />
                </div>
                <h3 className="text-xl font-semibold mb-4 text-white">
                  RESTful API
                </h3>
                <p className="text-gray-400">
                  Clean, well-documented API endpoints for seamless
                  communication between frontend and backend.
                </p>
              </CardContent>
            </Card>
            <Card className="text-center bg-gray-900 border-gray-700">
              <CardContent className="pt-6">
                <div className="text-purple-400 mb-4 flex justify-center">
                  <Database className="w-12 h-12" />
                </div>
                <h3 className="text-xl font-semibold mb-4 text-white">
                  Secure Database
                </h3>
                <p className="text-gray-400">
                  Robust data management with PostgreSQL ensuring data integrity
                  and security.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">
            Key Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              "User Authentication & Authorization",
              "Online Food Ordering System",
              "Table Reservation Management",
              "Admin Dashboard",
              "Real-time Order Tracking",
              "Payment Integration",
              "Responsive Mobile Design",
              "SEO Optimized",
              "Performance Monitoring",
            ].map((feature, index) => (
              <Card key={index} className="bg-gray-800 border-gray-700">
                <CardContent className="flex items-center gap-3 p-4">
                  <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                  <span className="text-gray-300">{feature}</span>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Developer */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6 text-blue-400">
            Built with Passion
          </h2>
          <p className="text-xl text-gray-300 leading-relaxed">
            This application represents a commitment to modern web development
            practices, clean code architecture, and exceptional user experience.
            Every component has been carefully crafted to ensure reliability,
            scalability, and maintainability.
          </p>
        </div>
      </section>
    </div>
  );
};

export default AboutDev;
