import { BrowserRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "sonner";
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
import Reservation from "./Pages/Reservation/Reservation";
import UserSettings from "./Pages/User/UserSettings";
import Profile from "./Pages/User/Profile";
import Contact from "./Pages/Contact/Contact";
import Header from "./Components/Header/Header";
import Footer from "./Components/Footer/Footer";
import { Cart } from "./Pages/Cart/Cart";
import { Terms } from "./Pages/About/Terms";
import FavouriteProducts from "./Pages/User/FavouriteProducts";
import Checkout from "./Pages/Checkout/Checkout";
import UserReservation from "./Pages/User/UserReservations";
import UserOrders from "./Pages/User/UserOrders"
import NotFound from "./Pages/NotFound/NotFound";
import { OpenRoute, AuthenticatedRoute } from "./Utils/RouteUtils";


const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 mins
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Toaster position="top-center" richColors />
        <Header />

        <Routes>
          {/* Open Routes - Accessible to everyone */}
          <Route path="/" element={<OpenRoute><Home /></OpenRoute>} />
          <Route path="/about" element={<OpenRoute><About /></OpenRoute>} />
          <Route path="/contact" element={<OpenRoute><Contact /></OpenRoute>} />
          <Route path="/about-dev" element={<OpenRoute><AboutDev /></OpenRoute>} />
          <Route path="/desserts" element={<OpenRoute><Desserts /></OpenRoute>} />
          <Route path="/desserts/:id" element={<OpenRoute><Dessert /></OpenRoute>} />
          <Route path="/doners" element={<OpenRoute><Doners /></OpenRoute>} />
          <Route path="/doners/:id" element={<OpenRoute><Doner /></OpenRoute>} />
          <Route path="/drinks" element={<OpenRoute><Drinks /></OpenRoute>} />
          <Route path="/drinks/:id" element={<OpenRoute><Drink /></OpenRoute>} />
          <Route path="/kebabs" element={<OpenRoute><Kebabs /></OpenRoute>} />
          <Route path="/kebabs/:id" element={<OpenRoute><Kebab /></OpenRoute>} />
          <Route path="/salads" element={<OpenRoute><Salads /></OpenRoute>} />
          <Route path="/salads/:id" element={<OpenRoute><Salad /></OpenRoute>} />
          <Route path="/login" element={<OpenRoute><Login /></OpenRoute>} />
          <Route path="/register" element={<OpenRoute><Register /></OpenRoute>} />
          <Route path="/terms" element={<OpenRoute><Terms /></OpenRoute>} />

          {/* Authenticated Routes - Only for authenticated users */}
          <Route path="/reservation" element={<AuthenticatedRoute><Reservation /></AuthenticatedRoute>} />
          <Route path="/profile" element={<AuthenticatedRoute><Profile /></AuthenticatedRoute>} />
          <Route path="/settings" element={<AuthenticatedRoute><UserSettings /></AuthenticatedRoute>} />
          <Route path="/favouriteProducts" element={<AuthenticatedRoute><FavouriteProducts /></AuthenticatedRoute>} />
          <Route path="/userReservations" element={<AuthenticatedRoute><UserReservation /></AuthenticatedRoute>} />
          <Route path="/checkout" element={<AuthenticatedRoute><Checkout /></AuthenticatedRoute>} />
          <Route path="/cart" element={<AuthenticatedRoute><Cart /></AuthenticatedRoute>} />
          <Route path="/userOrders" element={<AuthenticatedRoute><UserOrders /></AuthenticatedRoute>} />

          {/* Error Route - For nonexistent routes */}
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;