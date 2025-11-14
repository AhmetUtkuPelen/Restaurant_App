

import { Card, CardContent, CardHeader, CardTitle } from '@/Components/ui/card'
import { Separator } from '@/Components/ui/separator'
import { 
  FileText,
  Shield,
  CreditCard,
  Truck,
  AlertTriangle,
  Scale,
  Clock,
  Mail
} from 'lucide-react'

export const Terms = () => {
  const lastUpdated = "January 15, 2024"

  return (
    <div className="min-h-screen bg-slate-900 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4 flex items-center justify-center">
            <FileText className="h-10 w-10 mr-3 text-blue-400" />
            Terms of Service
          </h1>
          <p className="text-slate-400 text-lg">
            Last updated: {lastUpdated}
          </p>
        </div>

        {/* Introduction */}
        <Card className="bg-slate-800 border-slate-700 mb-8">
          <CardContent className="p-6">
            <p className="text-slate-300 leading-relaxed">
              Welcome to our restaurant's online ordering platform. These Terms of Service ("Terms") govern your use of our website, mobile application, and services. By accessing or using our services, you agree to be bound by these Terms. Please read them carefully.
            </p>
          </CardContent>
        </Card>

        {/* Terms Sections */}
        <div className="space-y-8">
          {/* Acceptance of Terms */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Scale className="h-5 w-5 mr-2 text-blue-400" />
                1. Acceptance of Terms
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <p>
                By creating an account, placing an order, or using any of our services, you acknowledge that you have read, understood, and agree to be bound by these Terms of Service and our Privacy Policy.
              </p>
              <p>
                We reserve the right to modify these Terms at any time. Changes will be effective immediately upon posting on our website. Your continued use of our services after any changes constitutes acceptance of the new Terms.
              </p>
            </CardContent>
          </Card>

          {/* Account Registration */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Shield className="h-5 w-5 mr-2 text-blue-400" />
                2. Account Registration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <p>
                To place orders and access certain features, you must create an account. You agree to:
              </p>
              <ul className="list-disc list-inside space-y-2 ml-4">
                <li>Provide accurate, current, and complete information</li>
                <li>Maintain and update your account information</li>
                <li>Keep your password secure and confidential</li>
                <li>Accept responsibility for all activities under your account</li>
                <li>Notify us immediately of any unauthorized use</li>
              </ul>
              <p>
                You must be at least 18 years old to create an account. We reserve the right to refuse service or terminate accounts at our discretion.
              </p>
            </CardContent>
          </Card>

          {/* Orders and Payment */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <CreditCard className="h-5 w-5 mr-2 text-blue-400" />
                3. Orders and Payment
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <div>
                <h4 className="font-semibold text-white mb-2">Order Placement</h4>
                <ul className="list-disc list-inside space-y-1 ml-4">
                  <li>All orders are subject to availability and acceptance</li>
                  <li>We reserve the right to refuse or cancel orders</li>
                  <li>Order confirmation does not guarantee acceptance</li>
                  <li>Prices are subject to change without notice</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-white mb-2">Payment Terms</h4>
                <ul className="list-disc list-inside space-y-1 ml-4">
                  <li>Payment is required at the time of order placement</li>
                  <li>We accept major credit cards, debit cards, and cash on delivery</li>
                  <li>All prices include applicable taxes unless otherwise stated</li>
                  <li>Delivery fees and service charges may apply</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Delivery and Pickup */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Truck className="h-5 w-5 mr-2 text-blue-400" />
                4. Delivery and Pickup
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <div>
                <h4 className="font-semibold text-white mb-2">Delivery Service</h4>
                <ul className="list-disc list-inside space-y-1 ml-4">
                  <li>Delivery is available within our designated service area</li>
                  <li>Estimated delivery times are approximate and not guaranteed</li>
                  <li>Delivery fees apply and vary by location</li>
                  <li>Minimum order requirements may apply for delivery</li>
                  <li>You must be available to receive your order at the specified address</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-white mb-2">Pickup Service</h4>
                <ul className="list-disc list-inside space-y-1 ml-4">
                  <li>Pickup orders must be collected within 30 minutes of notification</li>
                  <li>Valid ID may be required for order pickup</li>
                  <li>Uncollected orders may be disposed of without refund</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Cancellation and Refunds */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Clock className="h-5 w-5 mr-2 text-blue-400" />
                5. Cancellation and Refunds
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <div>
                <h4 className="font-semibold text-white mb-2">Order Cancellation</h4>
                <ul className="list-disc list-inside space-y-1 ml-4">
                  <li>Orders may be cancelled within 5 minutes of placement</li>
                  <li>Once food preparation begins, orders cannot be cancelled</li>
                  <li>We reserve the right to cancel orders due to ingredient unavailability</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-white mb-2">Refund Policy</h4>
                <ul className="list-disc list-inside space-y-1 ml-4">
                  <li>Refunds are processed for cancelled orders and quality issues</li>
                  <li>Refunds typically take 3-5 business days to process</li>
                  <li>Delivery fees are non-refundable unless the order is cancelled by us</li>
                  <li>Quality complaints must be reported within 24 hours</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* User Conduct */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2 text-blue-400" />
                6. User Conduct
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <p>You agree not to:</p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>Use our services for any illegal or unauthorized purpose</li>
                <li>Violate any laws or regulations</li>
                <li>Interfere with or disrupt our services or servers</li>
                <li>Attempt to gain unauthorized access to our systems</li>
                <li>Submit false or misleading information</li>
                <li>Harass, abuse, or harm our staff or other users</li>
                <li>Use our services to transmit spam or malicious content</li>
              </ul>
            </CardContent>
          </Card>

          {/* Limitation of Liability */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">7. Limitation of Liability</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <p>
                To the maximum extent permitted by law, we shall not be liable for any indirect, incidental, special, consequential, or punitive damages, including but not limited to loss of profits, data, or use, arising out of or relating to your use of our services.
              </p>
              <p>
                Our total liability for any claim arising out of or relating to these Terms or our services shall not exceed the amount you paid for the specific order giving rise to the claim.
              </p>
            </CardContent>
          </Card>

          {/* Privacy */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">8. Privacy</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <p>
                Your privacy is important to us. Our Privacy Policy explains how we collect, use, and protect your information when you use our services. By using our services, you consent to the collection and use of your information as described in our Privacy Policy.
              </p>
            </CardContent>
          </Card>

          {/* Governing Law */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">9. Governing Law</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <p>
                These Terms shall be governed by and construed in accordance with the laws of [Your State/Country], without regard to its conflict of law provisions. Any disputes arising under these Terms shall be subject to the exclusive jurisdiction of the courts in [Your City, State].
              </p>
            </CardContent>
          </Card>

          {/* Contact Information */}
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Mail className="h-5 w-5 mr-2 text-blue-400" />
                10. Contact Information
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <p>
                If you have any questions about these Terms of Service, please contact us:
              </p>
              <div className="space-y-2">
                <p><strong>Email:</strong> legal@restaurant.com</p>
                <p><strong>Phone:</strong> (555) 123-4567</p>
                <p><strong>Address:</strong> 123 Main Street, City, State 12345</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <Separator className="bg-slate-700 mb-6" />
          <p className="text-slate-400 text-sm">
            By continuing to use our services, you acknowledge that you have read and understood these Terms of Service.
          </p>
        </div>
      </div>
    </div>
  )
}
