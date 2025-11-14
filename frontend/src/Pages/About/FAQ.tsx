

import { 
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/Components/ui/accordion'
import { Card, CardContent, CardHeader, CardTitle } from '@/Components/ui/card'
import { Badge } from '@/Components/ui/badge'
import { 
  HelpCircle,
  Clock,
  MapPin,
  Phone,
  Mail,
  CreditCard,
  Truck,
  Calendar
} from 'lucide-react'

interface FAQItem {
  id: string
  question: string
  answer: string
  category: string
}

export const FAQ = () => {
  const faqItems: FAQItem[] = [
    {
      id: '1',
      question: 'What are your operating hours?',
      answer: 'We are open Monday to Sunday from 11:00 AM to 11:00 PM. Our kitchen closes 30 minutes before closing time. During holidays, hours may vary.',
      category: 'General'
    },
    {
      id: '2',
      question: 'Do you offer online ordering and delivery?',
      answer: 'Yes! You can place orders online through our website or mobile app. We offer delivery within a 5-mile radius with a minimum order of $15. Delivery typically takes 30-45 minutes.',
      category: 'Ordering'
    },
    {
      id: '3',
      question: 'Can I make a reservation for dining in?',
      answer: 'Absolutely! You can make reservations online through our website or by calling us directly. We recommend booking in advance, especially for weekends and holidays.',
      category: 'Reservations'
    },
    {
      id: '4',
      question: 'What types of food do you serve?',
      answer: 'We specialize in authentic Turkish cuisine including doners, kebabs, fresh salads, traditional desserts like baklava, and a variety of hot and cold beverages including Turkish tea and coffee.',
      category: 'Menu'
    },
    {
      id: '5',
      question: 'Do you have vegetarian and vegan options?',
      answer: 'Yes, we offer several vegetarian options including vegetable doner, falafel, various salads, and vegetarian kebabs. We also have vegan-friendly dishes - please ask our staff for recommendations.',
      category: 'Menu'
    },
    {
      id: '6',
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards (Visa, MasterCard, American Express), debit cards, cash, and digital payments including Apple Pay and Google Pay.',
      category: 'Payment'
    },
    {
      id: '7',
      question: 'Is there a delivery fee?',
      answer: 'Yes, we charge a $4.99 delivery fee for all orders. Free delivery is available for orders over $50 within our delivery zone.',
      category: 'Delivery'
    },
    {
      id: '8',
      question: 'How can I track my order?',
      answer: 'Once you place an order, you will receive an order confirmation with a tracking number. You can track your order status in real-time through our website or mobile app.',
      category: 'Ordering'
    },
    {
      id: '9',
      question: 'Do you cater for events and parties?',
      answer: 'Yes, we offer catering services for events, parties, and corporate meetings. Please contact us at least 24 hours in advance to discuss your catering needs and menu options.',
      category: 'Catering'
    },
    {
      id: '10',
      question: 'What is your cancellation policy?',
      answer: 'Orders can be cancelled within 5 minutes of placing them. After that, please contact us immediately. Reservations can be cancelled up to 2 hours before your scheduled time.',
      category: 'Policy'
    },
    {
      id: '11',
      question: 'Do you offer loyalty rewards or discounts?',
      answer: 'Yes! Join our loyalty program to earn points with every purchase. You also get a 10% discount on your first online order and special offers on your birthday.',
      category: 'Rewards'
    },
    {
      id: '12',
      question: 'Are your ingredients halal?',
      answer: 'Yes, all our meat products are halal certified. We take great care to ensure our ingredients meet halal standards and requirements.',
      category: 'Food Safety'
    }
  ]

  const categories = [...new Set(faqItems.map(item => item.category))]

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'General': return <Clock className="h-4 w-4" />
      case 'Ordering': return <Phone className="h-4 w-4" />
      case 'Reservations': return <Calendar className="h-4 w-4" />
      case 'Menu': return <HelpCircle className="h-4 w-4" />
      case 'Payment': return <CreditCard className="h-4 w-4" />
      case 'Delivery': return <Truck className="h-4 w-4" />
      default: return <HelpCircle className="h-4 w-4" />
    }
  }

  const getCategoryColor = (category: string) => {
    const colors = {
      'General': 'bg-blue-900/20 text-blue-300 border-blue-800',
      'Ordering': 'bg-green-900/20 text-green-300 border-green-800',
      'Reservations': 'bg-purple-900/20 text-purple-300 border-purple-800',
      'Menu': 'bg-orange-900/20 text-orange-300 border-orange-800',
      'Payment': 'bg-yellow-900/20 text-yellow-300 border-yellow-800',
      'Delivery': 'bg-red-900/20 text-red-300 border-red-800',
      'Catering': 'bg-pink-900/20 text-pink-300 border-pink-800',
      'Policy': 'bg-gray-900/20 text-gray-300 border-gray-800',
      'Rewards': 'bg-indigo-900/20 text-indigo-300 border-indigo-800',
      'Food Safety': 'bg-teal-900/20 text-teal-300 border-teal-800'
    }
    return colors[category as keyof typeof colors] || 'bg-gray-900/20 text-gray-300 border-gray-800'
  }

  return (
    <div className="min-h-screen bg-slate-900 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4 flex items-center justify-center">
            <HelpCircle className="h-10 w-10 mr-3 text-blue-400" />
            Frequently Asked Questions
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Find answers to common questions about our restaurant, menu, ordering, and services.
          </p>
        </div>

        {/* Contact Info */}
        <Card className="bg-slate-800 border-slate-700 mb-8">
          <CardHeader>
            <CardTitle className="text-white text-center">Still have questions?</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div className="flex items-center justify-center space-x-2 text-slate-300">
                <Phone className="h-4 w-4 text-blue-400" />
                <span>(555) 123-4567</span>
              </div>
              <div className="flex items-center justify-center space-x-2 text-slate-300">
                <Mail className="h-4 w-4 text-blue-400" />
                <span>info@restaurant.com</span>
              </div>
              <div className="flex items-center justify-center space-x-2 text-slate-300">
                <MapPin className="h-4 w-4 text-blue-400" />
                <span>123 Main St, City</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* FAQ Categories */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-white mb-4">Browse by Category</h2>
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <Badge 
                key={category} 
                className={`${getCategoryColor(category)} px-3 py-1`}
              >
                {getCategoryIcon(category)}
                <span className="ml-1">{category}</span>
              </Badge>
            ))}
          </div>
        </div>

        {/* FAQ Accordion */}
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-6">
            <Accordion type="single" collapsible className="space-y-2">
              {faqItems.map((item) => (
                <AccordionItem 
                  key={item.id} 
                  value={item.id}
                  className="border-slate-700"
                >
                  <AccordionTrigger className="text-white hover:text-blue-400 text-left">
                    <div className="flex items-start space-x-3">
                      <Badge className={`${getCategoryColor(item.category)} text-xs`}>
                        {item.category}
                      </Badge>
                      <span>{item.question}</span>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="text-slate-300 pt-4 pl-16">
                    {item.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </CardContent>
        </Card>

        {/* Bottom CTA */}
        <div className="text-center mt-12">
          <Card className="bg-gradient-to-r from-blue-900/20 to-slate-800 border-slate-700">
            <CardContent className="p-8">
              <h3 className="text-2xl font-semibold text-white mb-4">
                Ready to Order?
              </h3>
              <p className="text-slate-300 mb-6">
                Browse our delicious menu and place your order online for delivery or pickup.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors">
                  View Menu
                </button>
                <button className="border border-slate-600 text-slate-300 hover:bg-slate-700 px-6 py-3 rounded-lg font-medium transition-colors">
                  Make Reservation
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}