import { BrowserRouter, Route, Routes} from "react-router-dom";
import Home from "./Pages/Home/Home";
import About from "./Pages/About/About";
import Desserts from "./Pages/Couisine/Dessert/Desserts";
import Dessert from "./Pages/Couisine/Dessert/Dessert";
import Doners from "./Pages/Couisine/Doner/Doners";
import Doner from "./Pages/Couisine/Doner/Doner";
import Drinks from "./Pages/Couisine/Drink/Drinks";
import Drink from "./Pages/Couisine/Drink/Drink";
import Kebabs from "./Pages/Couisine/Kebab/Kebabs";
import Kebab from "./Pages/Couisine/Kebab/Kebab";
import Salads from "./Pages/Couisine/Salad/Salads";
import Register from "./Pages/Authentication/Register";
import Login from "./Pages/Authentication/Login";
import Salad from "./Pages/Couisine/Salad/Salad";
import AboutDev from "./Pages/About/AboutDev";
import Order from "./Pages/Order/Order";
import Reservation from "./Pages/Reservation/Reservation";
import UserSettings from "./Pages/User/UserSettings";
import Profile from "./Pages/User/Profile";
import AdminStock from "./Pages/Admin/AdminStock";
import Contact from "./Pages/Contact/Contact";
import Header from "./Components/Header/Header";
import Footer from "./Components/Footer/Footer";
import { Admin } from "./Pages/Admin/Admin";
import { Cart } from "./Pages/Cart/Cart";
import { OrderHistory } from "./Pages/User/OrderHistory";
import { FAQ } from "./Pages/About/FAQ";
import { Terms } from "./Pages/About/Terms";

function App() {
  return (
    <BrowserRouter>
    <Header/>

        <Routes>
          {/* Open Routes - Accessible to everyone */}

            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path ='/contact' element={<Contact/>} />
            <Route path="/about-dev" element={<AboutDev />} />
            <Route path="/desserts" element={<Desserts />} />
            <Route path="/desserts/:id" element={<Dessert />} />
            <Route path="/doners" element={<Doners />} />
            <Route path="/doners/:id" element={<Doner />} />
            <Route path="/drinks" element={<Drinks />} />
            <Route path="/drinks/:id" element={<Drink />} />
            <Route path="/kebabs" element={<Kebabs />} />
            <Route path="/kebabs/:id" element={<Kebab />} />
            <Route path="/salads" element={<Salads />} />
            <Route path="/salads/:id" element={<Salad />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/order_history" element={<OrderHistory />} />
            <Route path="/faq" element={<FAQ />} />
            <Route path="/terms" element={<Terms />} />


          {/* Protected Routes - Only for authenticated users */}

            <Route path="/order" element={<Order />} />
            <Route path="/reservation" element={<Reservation />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/settings" element={<UserSettings />} />


          {/* Admin Routes - Only for admin users */}

            <Route path="/admin" element={<Admin />} />
            <Route path="/admin/stock" element={<AdminStock />} />


          {/* Error Routes */}
          
        </Routes>
    <Footer/>
    </BrowserRouter>
  );
}

export default App;