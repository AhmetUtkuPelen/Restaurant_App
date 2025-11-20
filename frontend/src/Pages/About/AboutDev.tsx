import { Card, CardContent } from "@/Components/ui/card";
import {
  Database,
  Globe,
  Server,
  Smartphone,
} from "lucide-react";
import { FaReact } from "react-icons/fa";
import { SiTypescript } from "react-icons/si";
import { RiTailwindCssFill } from "react-icons/ri";
import { SiShadcnui } from "react-icons/si";
import { FaPython } from "react-icons/fa";
import { SiFastapi } from "react-icons/si";
import { SiSqlalchemy } from "react-icons/si";
import { SiPydantic } from "react-icons/si";
import { GrUserAdmin } from "react-icons/gr";



const AboutDev = () => {
  const frontendTech = [
    {
      name: "React",
      description: "A JavaScript library for building user interfaces",
      icon: <FaReact className="w-8 h-8" />,
      color: "text-blue-400",
    },
    {
      name: "TypeScript",
      description:
        "Typed superset of JavaScript that compiles to plain JavaScript",
      icon: <SiTypescript className="w-8 h-8" />,
      color: "text-blue-500",
    },
    {
      name: "TailwindCSS",
      description: "A utility-first CSS framework for rapid UI development",
      icon: <RiTailwindCssFill className="w-8 h-8" />,
      color: "text-cyan-400",
    },
    {
      name: "ShadCN",
      description:
        "Beautifully designed components built with Radix UI and Tailwind CSS",
      icon: <SiShadcnui className="w-8 h-8" />,
      color: "text-gray-400",
    },
  ];

  const backendTech = [
    {
      name: "Python",
      description: "High-level , multi functional programming language",
      icon: <FaPython className="w-8 h-8" />,
      color: "text-yellow-400",
    },
    {
      name: "FastAPI",
      description: "Modern , async , fast web framework for building APIs with Python",
      icon: <SiFastapi className="w-8 h-8" />,
      color: "text-green-400",
    },
    {
      name: "SQLAlchemy",
      description: "Python SQL toolkit and Object-Relational Mapping library",
      icon: <SiSqlalchemy className="w-8 h-8" />,
      color: "text-red-400",
    },
    {
      name: "Pydantic",
      description: "Data validation and settings management using Python type annotations",
      icon: <SiPydantic className="w-8 h-8" />,
      color: "text-purple-400",
    },
    {
      name: "SqlAdmin",
      description: "SQLAdmin is a flexible Admin interface for FastAPi - Starlette SQLAlchemy models",
      icon: <GrUserAdmin className="w-8 h-8" />,
      color: "text-purple-400",
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
            An Industrial Engineer who also likes to code using modern technologies like Python and Typescript/Javascript.
          </p>
        </div>
      </section>

      {/* Tech Stack Overview */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-6 text-blue-400">
              Tech Stack
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              This restaurant application was built using cutting-edge modern
              technologies to ensure scalability, performance, and
              maintainability.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Frontend */}
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-8">
                <div className="flex items-center gap-3 mb-8">
                  <Globe className="w-8 h-8 text-blue-400" />
                  <h3 className="text-3xl font-bold text-blue-400">FRONT END</h3>
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

            {/* Backend */}
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-8">
                <div className="flex items-center gap-3 mb-8">
                  <Server className="w-8 h-8 text-green-400" />
                  <h3 className="text-3xl font-bold text-green-400">BACK END</h3>
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

      {/* Architecture */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-6xl mx-auto px-4">
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
              "Payment Integration",
              "Responsive Mobile Design",
              "SEO Optimized",
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
            Built with Passion and Curiosity for Web Development
          </h2>
          <p className="text-xl text-gray-300 leading-relaxed">
            If you would like to get in touch with  me , you can use the Contact form in Contact Page or simply click the Mail Icon In the Footer
          </p>
        </div>
      </section>
    </div>
  );
};

export default AboutDev;
