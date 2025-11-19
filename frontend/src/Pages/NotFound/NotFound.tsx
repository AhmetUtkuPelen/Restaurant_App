import { Button } from "@/Components/ui/button";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";


const NotFound = () => {

    const navigate = useNavigate();

    const HandleGoHome = () => {
        toast.message("You are going Home page !")
        setTimeout(() => {
            navigate('/')
        }, 2000);
    }

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-4xl font-bold mb-4 text-red-600">404 - Not Found</h1>
      <p className="text-lg mb-4">The page you are looking for does not exist.</p>
      <Button onClick={() => HandleGoHome()}>Go Back</Button>
    </div>
  );
};

export default NotFound;